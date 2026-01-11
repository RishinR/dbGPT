import re
import asyncpg
from config import settings
from groq_client import groq_client


class PostgresDB:
    def __init__(self):
        self.conn = None
        self.table_details = None
        self.schema = "public"

    async def connect(self):
        try:
            self.conn = await asyncpg.connect(settings.POSTGRES_DB_URI)
            self.schema = settings.DB_SCHEMA
            print("Connected to postgres db!")
        except Exception as e:
            print(f"Connection to postgres DB failed: {e}")

    async def close(self):
        if not self.conn:
            print("Connection to db is not yet established!")
            return
        try:
            await self.conn.close()
            print("Connection to postgres db closed successfully!")
        except Exception as e:
            print(f"Closing connection to DB failed: {e}")

    async def fetch_all(self, query: str):
        if not self.conn:
            print("Connection to db is not yet established!")
            return
        try:
            rows = await self.conn.fetch(query)
            rows = [dict(row) for row in rows]
            return rows
        except Exception as e:
            print(f"Error on executing the SQL query: {query}")

    async def get_all_tables(self):
        if not self.conn:
            print("Connection to db is not yet established!")
            return
        try:
            get_all_tables_query = f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = '{self.schema}'
                AND table_type = 'BASE TABLE';
            """
            tables = await self.fetch_all(get_all_tables_query)
            return tables
        except Exception as e:
            print(f"Error in getting all tables from the DB: {e}")

    async def load_table_details(self):
        tables = await self.get_all_tables()
        if not tables:
            print("Tables list is empty!")
            return False
        table_details = []
        try:
            for table in tables:
                table_name = table["table_name"]

                # Get the table information
                get_table_details = f"""
                    SELECT 
                        column_name,
                        data_type
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """
                table_info = await self.fetch_all(get_table_details)

                # Take a sample row from the table
                get_sample_row = f"""
                    SELECT *
                    FROM {table_name}
                    LIMIT 1;    
                """
                sample_row = await self.fetch_all(get_sample_row)

                # Append to table details array
                table_details.append(
                    {
                        "table_name": table_name,
                        "table_info": table_info,
                        "sample_row": sample_row,
                    }
                )
            self.table_details = table_details
            return True
        except Exception as e:
            print(f"Error in getting table info from DB: {e}")

    async def generate_sql_query(self, user_query):
        try:
            system_prompt = """
                You are an expert SQL query generator specializing in PostgreSQL databases. Your task is to generate a correct and efficient SQL query that can retrieve the data needed to answer a user's question.

                Input:
                - user_query: A natural language question or request describing the data the user wants to extract.
                - schema_name: The PostgreSQL schema in which the tables reside.
                - table_details: A list of JSON objects, each representing a table in the database. Each JSON object contains:
                    - table_name: The name of the table.
                    - table_information: The list of columns in the table along with their data types.
                    - sample_row: An example row of data from the table that demonstrates the kind of data it contains.

                Output:
                A SQL query in PostgreSQL syntax that accurately retrieves the information needed to answer the user_query, based on the provided table structures and sample data.
                The output should be inside the ```sql ``` block. Only return this and nothing else.

                Instructions:
                Analyze the user_query carefully to understand what data is required.
                Use the table names, column names, types, and sample data to construct the SQL query.
                Ensure the SQL query is syntactically correct for PostgreSQL and optimized for accuracy and clarity.
                Return only the SQL query as the output, without explanations or additional text.
            """

            user_prompt = f"""
                user_query: {user_query},
                schema_name: {self.schema}
                table_details: {self.table_details}
            """

            history = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            response = groq_client.get_chat_completion(history)
            # response = await gemini_client.get_chat_completion(history)
            if response:
                response = response.split("```sql")[1].split("```")[0].strip()
                return response
            return None
        except Exception as e:
            print(f"Failed to generate sql query: {e}")


postgres_db = PostgresDB()
