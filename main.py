import asyncio
from config import settings
from db import postgres_db
from mongodb import mongo_db
from orchestration_agent import OrchestrationAgent
from user_response_agent import user_response_agent


async def main() -> None:
    # Select database based on configuration
    db_type = settings.DB_TYPE
    db = None
    
    if db_type == "postgres":
        print("Using PostgreSQL database...")
        db = postgres_db
        await db.connect()
        load_status = await db.load_table_details()
        if not load_status:
            print("Schema doesn't have any tables, please try creating one or add a schema in the URI which contains tables")
            return
    elif db_type == "mongodb":
        print("Using MongoDB database...")
        db = mongo_db
        await db.connect()
        load_status = await db.load_collection_details()
        if not load_status:
            print("Database doesn't have any collections, please create some collections first")
            return
    else:
        print(f"Unsupported database type: {db_type}. Please set DB_TYPE to 'postgres' or 'mongodb'")
        return

    # Initialize orchestration agent
    orchestration_agent = OrchestrationAgent()

    print(f"\ndbGPT Assistant ready! (Using {db_type.upper()})")
    print("Type your questions or 'exit' to quit.\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Shutting down application!")
            break

        try:
            # Enhance user_query based on previous conversations
            enhanced_user_query = await orchestration_agent.enhance_user_query(user_query)
            
            # Generate and execute query based on database type
            if db_type == "postgres":
                sql_query = await db.generate_sql_query(enhanced_user_query) or ""
                # print(f"SQL Query Generated:\n{sql_query}")
                data = await db.fetch_all(sql_query)
                query_str = sql_query
            else:  # mongodb
                mongo_query = await db.generate_mongo_query(enhanced_user_query)
                # print(f"MongoDB Query Generated:\n{mongo_query}")
               
                if mongo_query:
                    if mongo_query.get("allowed") is False:
                        data = []
                        raise Exception("The requested operation is not allowed.")
                    data = await db.execute_query(mongo_query)
                    query_str = str(mongo_query)
                else:
                    data = []
                    query_str = ""

            # Generate user response
            response = (
                await user_response_agent.generate_user_response(
                    user_query, query_str, data
                )
                or ""
            )
            
            orchestration_agent.history.append({"role": "assistant", "content": response})
            print(f"Assistant: {response}\n")
            
        except Exception as e:
            print(f"Error processing query: {e}\n")

    # Close DB connection
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())