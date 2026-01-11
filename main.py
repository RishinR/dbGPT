import asyncio
from db import postgres_db
from orchestration_agent import OrchestrationAgent
from user_response_agent import user_response_agent


async def main() -> None:
    # Connect to DB
    await postgres_db.connect()

    # Load table details
    await postgres_db.load_table_details()

    # Initialise orchestration agent
    orchestration_agent = OrchestrationAgent()

    while True:
        user_query = input("You: ")
        if user_query == "exit":
            print("Shutting down application!")
            break

        # Enhance user_query based on previous conversations
        enhanced_user_query = await orchestration_agent.enhance_user_query(user_query)
        # print(f"Enhanced user query:\n{enhanced_user_query}")

        sql_query = await postgres_db.generate_sql_query(enhanced_user_query) or ""
        # print(f"SQL Query Generated:\n{sql_query}")

        data = await postgres_db.fetch_all(sql_query)
        response = (
            await user_response_agent.generate_user_response(
                user_query, sql_query, data
            )
            or ""
        )
        orchestration_agent.history.append({"role": "assistant", "content": response})
        print(f"Assistant: {response}")
    # Close DB connection
    await postgres_db.close()


if __name__ == "__main__":
    asyncio.run(main())
