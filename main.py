from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from log import logger
from scrapper import LinkedInScraper
from ai import LinkedInMessageGenerator

load_dotenv()

app = Flask(__name__)


class ProfileRequest(BaseModel):
    username: str
    password: str
    profile_url: str


@app.route("/create_message", methods=["POST"])
def create_connection_message():
    try:
        data = request.get_json()
        profile_request = ProfileRequest(**data)

        scrapper = LinkedInScraper()
        ai = LinkedInMessageGenerator()

        profile_data = scrapper.get_profile_data(
            profile_request.username,
            profile_request.password,
            profile_request.profile_url,
        )
        message = ai.generate_connection_message(profile_data)

        response = {
            "connection_message": message,
            "profile_data": profile_data,
        }
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"details": e.errors()}), 400
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"details": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
