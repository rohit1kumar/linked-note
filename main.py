from fastapi import FastAPI, status
from pydantic import BaseModel
from dotenv import load_dotenv
from scrapper import LinkedInScraper
from ai import LinkedInMessageGenerator
from log import logger

app = FastAPI()
load_dotenv()


class ProfileRequest(BaseModel):
    username: str
    password: str
    profile_url: str


@app.post("/create_connection_message")
def create_connection_message(request: ProfileRequest):
    try:
        scraper = LinkedInScraper()
        ai = LinkedInMessageGenerator()

        profile_data = scraper.get_profile_data(
            request.username,
            request.password,
            request.profile_url,
        )
        connection_message = ai.generate_connection_message(profile_data)

        return {
            "profile_data": profile_data,
            "connection_message": connection_message,
        }
    except Exception as e:
        logger.error(f"Error analyzing profile: {str(e)}")
        return {
            "error": "Failed to analyze profile"
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
