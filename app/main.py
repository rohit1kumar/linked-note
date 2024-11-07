import os
import json
import redis
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel, ValidationError
from scraper import LinkedInScraper
from message_generator import LinkedInMessageGenerator

load_dotenv()

app = Flask(__name__)

cache = redis.from_url(os.getenv("REDIS_URL"))


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

        # Use Redis cache for storing scraped data
        cache_key = f"profile_data_{profile_request.profile_url}"
        cached_profile_data = cache.get(cache_key)

        if cached_profile_data:
            app.logger.info("Cache hit")
            profile_data = json.loads(cached_profile_data.decode("utf-8"))
        else:
            scrapper = LinkedInScraper(
                profile_request.username,
                profile_request.password,
            )
            profile_data = scrapper.get_profile_data(profile_request.profile_url)

            if not profile_data:
                return jsonify({"details": "Not able to scrape profile"}), 500

            # Cache the scraped profile data
            cache.set(cache_key, profile_data)
            cache.expire(cache_key, 86400)  # Expire in 24 hours

        message_generator = LinkedInMessageGenerator()
        message = message_generator.generate_connection_message(profile_data)

        response = {
            "connection_message": message,
            "profile_data": profile_data,
        }
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"details": e.errors()}), 400
    except Exception as e:
        print(e)
        app.logger.error(f"Error creating connection message: {str(e)}")
        return jsonify({"details": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
