import asyncio
from db import postgres_db
from user_response_agent import user_response_agent


async def main() -> None:
    await postgres_db.connect()

    # Load table details
    await postgres_db.load_table_details()

    user_query = input("You: ")
    sql_query = await postgres_db.generate_sql_query(user_query)
    if sql_query:
        data = await postgres_db.fetch_all(sql_query)
        response = await user_response_agent.generate_user_response(
            user_query, sql_query, data
        )
        print(f"Assistant: {response}")
        return
    await postgres_db.close()


if __name__ == "__main__":
    asyncio.run(main())
