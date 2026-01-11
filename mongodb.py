from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from groq_client import groq_client
import json


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection_details = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            # Extract database name from URI or use default
            db_name = settings.MONGODB_DATABASE or "default_db"
            self.db = self.client[db_name]
            # Test connection
            await self.client.admin.command('ping')
            print(f"Connected to MongoDB database: {db_name}!")
        except Exception as e:
            print(f"Connection to MongoDB failed: {e}")

    async def close(self):
        if self.client is None:
            print("Connection to MongoDB is not yet established!")
            return
        try:
            self.client.close()
            print("Connection to MongoDB closed successfully!")
        except Exception as e:
            print(f"Closing connection to MongoDB failed: {e}")

    async def get_all_collections(self):
        if self.db is None:
            print("Connection to MongoDB is not yet established!")
            return []
        try:
            collections = await self.db.list_collection_names()
            return [{"collection_name": col} for col in collections]
        except Exception as e:
            print(f"Error in getting all collections from MongoDB: {e}")
            return []

    async def load_collection_details(self):
        collections = await self.get_all_collections()
        if not collections:
            print("Collections list is empty!")
            return False
        
        collection_details = []
        try:
            for collection in collections:
                collection_name = collection["collection_name"]
                col = self.db[collection_name]

                # Get sample documents (first 2 for schema inference)
                sample_docs = await col.find().limit(2).to_list(length=2)
                
                # Infer schema from sample documents
                schema = self._infer_schema(sample_docs)

                # Get document count
                doc_count = await col.count_documents({})

                # Create a simplified sample (only first document, with truncated values)
                simplified_sample = None
                if sample_docs:
                    simplified_sample = self._simplify_document(sample_docs[0])

                collection_details.append({
                    "collection_name": collection_name,
                    "schema": schema,
                    "sample_document": simplified_sample,
                    "document_count": doc_count
                })
            
            self.collection_details = collection_details
            return True
        except Exception as e:
            print(f"Error in getting collection info from MongoDB: {e}")
            return False

    def _infer_schema(self, documents):
        """Infer schema structure from sample documents"""
        if not documents:
            return {}
        
        schema = {}
        for doc in documents:
            for key, value in doc.items():
                if key not in schema:
                    schema[key] = type(value).__name__
        return schema

    def _simplify_document(self, doc, max_str_length=50):
        """Simplify a document by truncating long strings and nested structures"""
        if not doc:
            return None
        
        simplified = {}
        for key, value in doc.items():
            if isinstance(value, str) and len(value) > max_str_length:
                simplified[key] = value[:max_str_length] + "..."
            elif isinstance(value, (list, dict)):
                # For complex nested structures, just show the type
                simplified[key] = f"<{type(value).__name__}>"
            else:
                simplified[key] = value
        return simplified

    async def execute_query(self, query_obj):
        """Execute a MongoDB query"""
        if self.db is None:
            print("Connection to MongoDB is not yet established!")
            return []
        
        try:
            collection_name = query_obj.get("collection")
            operation = query_obj.get("operation", "find")
            query = query_obj.get("query", {})
            projection = query_obj.get("projection", None)
            sort = query_obj.get("sort", None)
            limit = query_obj.get("limit", 100)
            
            col = self.db[collection_name]
            
            if operation == "find":
                cursor = col.find(query, projection)
                if sort:
                    cursor = cursor.sort(sort)
                if limit:
                    cursor = cursor.limit(limit)
                results = await cursor.to_list(length=limit)
                return results
            
            elif operation == "aggregate":
                pipeline = query_obj.get("pipeline", [])
                results = await col.aggregate(pipeline).to_list(length=limit)
                return results
            
            elif operation == "count":
                count = await col.count_documents(query)
                return [{"count": count}]
            
            else:
                print(f"Unsupported operation: {operation}")
                return []
                
        except Exception as e:
            print(f"Error executing MongoDB query: {e}")
            return []

    async def generate_mongo_query(self, user_query):
        try:
            system_prompt = """
You are an expert MongoDB query generator. Your task is to generate a correct and efficient MongoDB query object that can retrieve the data needed to answer a user's question.

Input:
- user_query: A natural language question or request describing the data the user wants to extract.
- collection_details: A list of JSON objects, each representing a collection in the MongoDB database. Each object contains:
    - collection_name: The name of the collection.
    - schema: Inferred field types from sample documents.
    - sample_document: A simplified example document from the collection.
    - document_count: Total number of documents in the collection.

Output:
A MongoDB query object in JSON format that accurately retrieves the information needed to answer the user_query. The output should be inside a ```json``` block. Only return this and nothing else.

The query object should have this structure:
{
    "collection": "collection_name",
    "operation": "find|aggregate|count",
    "query": {},  // MongoDB query filter (for find/count)
    "projection": {},  // Optional: fields to return
    "sort": [["field", 1]],  // Optional: sort order (1 for asc, -1 for desc)
    "limit": 100,  // Optional: max documents to return
    "pipeline": []  // For aggregation operations
    "allowed": boolean // Safe operation or not
}

Instructions:
- Analyze the user_query carefully to understand what data is required.
- Never disclose any database credentials or sensitive information.
- Never disclose ObjectId or internal MongoDB fields.
- Use the collection names, schemas, and sample documents to construct the query.
- If the user asks to delete or modify data, respond with allowed = false and rest None.
- For simple queries, use "find" operation with query filters.
- For complex queries requiring grouping, calculations, or joins, use "aggregate" operation.
- Keep the limit reasonable (default 100, but adjust based on the query).
- Ensure the query is syntactically correct for MongoDB.
- Return only the query object as JSON, without explanations or additional text.
"""

            # Create a more concise representation of collection details
            concise_details = []
            for col in self.collection_details:
                concise_details.append({
                    "collection_name": col["collection_name"],
                    "schema": col["schema"],
                    "sample_document": col["sample_document"],
                    "document_count": col["document_count"]
                })

            user_prompt = f"""
user_query: {user_query}
collection_details: {json.dumps(concise_details, default=str, indent=2)}
"""

            history = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            response = groq_client.get_chat_completion(history)
            if response:
                response = response.split("```json")[1].split("```")[0].strip()
                return json.loads(response)
            return None
        except Exception as e:
            print(f"Failed to generate MongoDB query: {e}")
            return None


mongo_db = MongoDB()