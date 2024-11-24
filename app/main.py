import os
import json
import redis
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel, ValidationError
from scraper import LinkedInScraper
from message_generator import LinkedInMessageGenerator
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
# cache = redis.from_url(os.getenv("REDIS_URL"))


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

        # # Use Redis cache for storing scraped data
        # cache_key = f"profile_data_{profile_request.profile_url}"
        # cached_profile_data = cache.get(cache_key)

        # if cached_profile_data:
        #     app.logger.info("Cache hit")
        #     profile_data = json.loads(cached_profile_data.decode("utf-8"))
        # else:
        #     scrapper = LinkedInScraper(
        #         profile_request.username,
        #         profile_request.password,
        #     )
        #     profile_data = scrapper.get_profile_data(profile_request.profile_url)

        #     if not profile_data:
        #         return jsonify({"details": "Not able to scrape profile"}), 500

        #     # Cache the scraped profile data
        #     cache.set(cache_key, profile_data)
        #     cache.expire(cache_key, 86400)  # Expire in 24 hours

        # message_generator = LinkedInMessageGenerator()
        # message = message_generator.generate_connection_message(profile_data)

        response = {
            "connection_message": "Hello Aniket, I'm impressed by your work with LimeChat and your expertise in CX and marketing. Would love to connect and discuss potential collaborations in the future. Best regards.\n\n[Your Name]",
            "profile_data": {
                "headline": "Forbes 30u30 | Co-Founder, LimeChat | CX and Marketing Advisor to 300+ Brands | Building Enterprise-Grade Gen AI Support",
                "name": "Aniket Bajpai",
                "posts": [
                    "\"Why should I provide support on WhatsApp? It's too expensive.\"This was the biggest hesitation for many business leaders when considering WhatsApp as their main customer support channel. As a result, customers were stuck navigating outdated support through emails and calls.But here's the game-changer: Starting this November, service conversations on WhatsApp will be COMPLETELY free.When given the choice, 80% of customers prefer WhatsApp over emails and calls. This shift opens up incredible opportunities for brands to enhance their CX.With Gen AI-powered solutions on WhatsApp, you can elevate CX and drive down costs at the same time.This is all part of Meta\u2019s broader strategy to position WhatsApp as a channel for meaningful conversations vs spamming users.We\u2019re standing at the forefront of a customer experience revolution. It\u2019s thrilling to see WhatsApp leading the charge.Which brands do you wish offered support on WhatsApp?",
                    "Diwali has been a special tradition for us at LimeChat since we started building our team in 2021. Diwali season is one of the busiest times in e-commerce, and our team works hard from July to October to make sure everything runs smoothly.This year felt extra special. We didn\u2019t just reach our goals\u2014we achieved more than ever before. From record-breaking sales to stronger customer relationships and closer team bonds, 2024 has been our best year yet.Our Diwali party is a time to relax, celebrate our efforts, and enjoy with friends and family before a well-earned break.Wishing everyone a Diwali 2024 filled with happiness and light!",
                    "The last step of manual effort in quick commerce is about to be over.Swiggy is set to launch shopping lists!You will be able to upload an image of your shopping list - the app will scan it and show all the items to add to cart. Now I will create a grocery list for Diwali pooja or daily groceries with ChatGPT\u2014and upload it all to Instamart as a screenshot or note.No more manual item-by-item searching; just snap, upload, and shop.This might be big enough to make me switch back from Blinkit to Instamart!",
                    "The Bhavish Aggarwal vs. Kunal Kamra clash taught me one big thing.Customer experience can make or break a brand.Ola Electric had arguably one of the best IPOs this year.They listed at a price lower than their valuation and then saw amazing growth in the public markets after listing.This was because they were the market leader in the rapidly growing EV space.But now the focus has shifted away from Ola Electric\u2019s products, profits, and sales to its service. And that has led to a staggering 50% drop in stock price.Here\u2019s the lesson:Your brand cannot be defined by service issues, since the customer narrative isn\u2019t forgiving. Sales can be benchmarked against past performance, but service is held to perfection - even one dissatisfied customer keeps the narrative going.Ola\u2019s story went from \u201cditch your old bike for our sleek, new EV\u201d to \u201cwe\u2019re addressing 99% of reported issues.\u201d It\u2019s a powerful reminder: no matter how innovative the product, CX needs to keep pace.",
                    "We\u2019re hiring for our Customer Success team at LimeChat!Join us to help top brands like Mamaearth, Porter, and Cult Sport create amazing Gen AI experiences on WhatsApp. At LimeChat, you'll grow fast, work with a team of A-players, and make an impact every day.Ready to be part of our journey? Apply at the link in the comments!hashtag#Hiring hashtag#CustomerSuccess hashtag#LimeChat hashtag#JoinOurTeam",
                ],
            },
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
