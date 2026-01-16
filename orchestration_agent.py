from openai_client import openai_client


class OrchestrationAgent:
    def __init__(self):
        self.system_prompt = """
            You are a query enhancement assistant. Your task is to rewrite the user's query into a clear, detailed, and unambiguous form **only when required**, using the prior conversation context and previously available information.

            ### Instructions

            1. Analyze the latest user query together with the conversation history.
            2. Enhance the user query by adding missing details, clarifying intent, and resolving ambiguities **only using information already present in the conversation**.
            3. Do **not** introduce new assumptions or information that is not explicitly stated or implied in the prior context.

            ### Rules

            * The output must contain **only the enhanced version of the user's query**.
            * If the original user query is already clear and complete, return it as-is (without modification).
            * If the user requests to delete, update, modify, or otherwise change any content, deny the request and restrict the enhancement to read-only actions (e.g., retrieve, summarize, or clarify information).

            ### Output Constraints

            * The output **must be only a valid JSON object**.
            * The output **must be wrapped inside a `json` code block**.
            * Do **not** include any additional text or explanation outside the JSON block.

            ### Output Format

            ```json
            {
            "enhanced_user_query": "string"
            }
            ```
        """
        self.history = [{"role": "system", "content": self.system_prompt}]

    async def enhance_user_query(self, user_query):
        try:
            user_prompt = f"""
                user query: {user_query}
            """
            self.history.append({"role": "user", "content": user_prompt})
            response = await openai_client.get_chat_completion(self.history)
            if response:
                response = response.split("```json")[1].split("```")[0].strip()
                return response
            return ""
        except Exception as e:
            print(f"Failed to generate enhanced user query: {e}")
