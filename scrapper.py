import os
from log import logger
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


class LinkedInScraper:
    def get_profile_data(self, username: str, password: str, profile_url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                # Login
                page.goto("https://www.linkedin.com/login")
                page.fill("#username", username)
                page.fill("#password", password)
                page.click('button[type="submit"]')
                page.wait_for_load_state("domcontentloaded")

                # Check if login was unsuccessful
                if "login" in page.url:
                    raise Exception("Login failed")

                # # Go to profile page
                page.goto(profile_url)
                page.wait_for_load_state("domcontentloaded")

                # # Get profile data
                name = page.text_content(".text-heading-xlarge")
                headline = page.text_content(".text-body-medium")

                feeds_url = f"{profile_url}/recent-activity/all/"
                # Go to feeds page
                page.goto(feeds_url)
                page.wait_for_load_state("domcontentloaded")

                posts = []
                page.wait_for_selector(".feed-shared-update-v2", timeout=10000)
                post_elements = page.query_selector_all(".feed-shared-update-v2")
                for post in post_elements[:2]:
                    try:
                        post_content_element = post.query_selector(
                            ".update-components-text"
                        )
                        if post_content_element:
                            post_text = post_content_element.text_content()
                            posts.append(post_text.strip())
                    except Exception as e:
                        logger.error("Error getting post text, skipping", e)
                        continue

                return {
                    "name": name.strip(),
                    "headline": headline.strip(),
                    "posts": posts,
                }

            except Exception as e:
                logger.error(f"Error: {str(e)}")
            finally:
                browser.close()


# if __name__ == "__main__":
#     scraper = LinkedInScraper()
#     username = os.getenv("LINKEDIN_USERNAME")
#     password = os.getenv("LINKEDIN_PASSWORD")
#     profile_url = "https://www.linkedin.com/in/aniket-bajpai"

#     data = scraper.get_profile_data(username, password, profile_url)
#     print(data)
