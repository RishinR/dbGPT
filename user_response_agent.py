from groq_client import groq_client


class UserResponseAgent:
    async def generate_user_response(self, user_query, sql_query, results):
        system_prompt = """
            You are an expert assistant in answering user queries. 
            Provide a clear and concise response to the user's question using the SQL query generated and the results obtained from the database. 
            Ensure your answer is accurate, easy to understand, and directly relevant to the user's query.
        """

        user_prompt = f"""
            user query: {user_query},
            sql query generated: {sql_query},
            db result: {results}
        """

        history = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = groq_client.get_chat_completion(history)
        return response

user_response_agent = UserResponseAgent()