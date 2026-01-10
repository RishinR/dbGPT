import json
import asyncio
from db import postgres_db


async def main() -> None:
    await postgres_db.connect()

    await postgres_db.load_table_details()
    output = await postgres_db.generate_sql_query(
        "What is the total no of male students in the class?"
    )
    print(output)

    await postgres_db.close()


if __name__ == "__main__":
    asyncio.run(main())
