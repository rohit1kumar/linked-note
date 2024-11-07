import os
from openai import OpenAI
from dotenv import load_dotenv
from log import logger

load_dotenv()


class LinkedInMessageGenerator:
    def __init__(self):
        self.ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _get_formated_posts(self, profile_data):
        formatted_posts = ""
        posts = profile_data["posts"][:5]
        for i in range(len(posts)):
            post = posts[i]
            formatted_posts += "Post " + str(i + 1) + ": " + post + "\n"
        return formatted_posts.strip()

    def _create_prompt(self, profile_data):
        formated_posts = self._get_formated_posts(profile_data)
        return f"""
        Create a 2-line professional, easy to understand personalized LinkedIn connection request message based on following profile data:

        Name: {profile_data['name']}
        Headline: {profile_data['headline']}
        Recent posts: {formated_posts}
        """

    def _create_ai_response(self, prompt):
        response = self.ai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL") or "gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        logger.info("AI response generated")
        return response.choices[0].message.content

    def generate_connection_message(self, profile_data):
        prompt = self._create_prompt(profile_data)
        return self._create_ai_response(prompt)
