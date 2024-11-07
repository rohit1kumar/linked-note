from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from scraper import LinkedInScraper
from message_generator import LinkedInMessageGenerator

load_dotenv()

app = Flask(__name__)


class ProfileRequest(BaseModel):
    username: str
    password: str
    profile_url: str


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_message", methods=["POST"])
def create_connection_message():
    try:
        data = request.get_json()
        profile_request = ProfileRequest(**data)
        app.logger.info(f"Request: {profile_request.dict()}")

        scrapper = LinkedInScraper(profile_request.username, profile_request.password)
        message_generator = LinkedInMessageGenerator()

        profile_data = scrapper.get_profile_data(profile_request.profile_url)

        if not profile_data:
            return jsonify({"details": "Not able to scrape profile"}), 500

        message = message_generator.generate_connection_message(profile_data)
    
        response = {
            "connection_message": message,
            "profile_data": profile_data,
        }
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"details": e.errors()}), 400
    except Exception as e:
        app.logger.error(f"Error creating connection message: {str(e)}")
        return jsonify({"details": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
