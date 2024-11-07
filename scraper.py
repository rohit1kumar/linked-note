import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from log import logger

load_dotenv()


class LinkedInScraper:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_profile_data(self, profile_url: str) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                self._login(page)
                self._navigate_to_profile(page, profile_url)
                profile_data = self._scrape_profile_data(page)
                self._navigate_to_recent_posts(page, profile_url)
                profile_data["posts"] = self._scrape_recent_posts(page)
                return profile_data
            except Exception as e:
                logger.error(f"Error scraping profile: {str(e)}")
                return {
                    "name": "Failed to fetch",
                    "headline": "Failed to fetch",
                    "posts": [],
                }
            finally:
                browser.close()

    def _login(self, page):
        page.goto("https://www.linkedin.com/login")
        page.fill("#username", self.username)
        page.fill("#password", self.password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("domcontentloaded")

        if "login" in page.url:
            logger.error("Login failed")
            raise Exception("Login failed")

        logger.info("Login successful, going to profile page")

    def _navigate_to_profile(self, page, profile_url):
        page.goto(profile_url)
        page.wait_for_load_state("domcontentloaded")

    def _scrape_profile_data(self, page):
        name = page.text_content(".text-heading-xlarge")
        headline = page.text_content(".text-body-medium")

        if not name or not headline:
            raise Exception("Failed to fetch name or headline from profile.")

        logger.info(f"Scraped profile: {name} - {headline}")
        return {
            "name": name.strip(),
            "headline": headline.strip(),
        }

    def _navigate_to_recent_posts(self, page, profile_url):
        feeds_url = f"{profile_url}/recent-activity/all/"
        page.goto(feeds_url)
        page.wait_for_load_state("domcontentloaded")

    def _scrape_recent_posts(self, page):
        posts = []
        page.wait_for_selector(".feed-shared-update-v2", timeout=10000)
        post_elements = page.query_selector_all(".feed-shared-update-v2")

        if not len(post_elements):
            logger.warning("No posts found")
        else:
            for post in post_elements[:5]:
                try:
                    post_content_element = post.query_selector(
                        ".update-components-text"
                    )
                    if post_content_element:
                        post_text = post_content_element.text_content()
                        posts.append(post_text.strip())
                except Exception as e:
                    logger.error(f"Error getting post text {str(e)}, skipping")
                    continue

        logger.info(f"Scraped {len(posts)} posts")
        return posts


# if __name__ == "__main__":
#     username = os.getenv("LINKEDIN_USERNAME")
#     password = os.getenv("LINKEDIN_PASSWORD")
#     profile_url = "https://www.linkedin.com/in/aniket-bajpai"

#     scraper = LinkedInScraper(username, password)
#     data = scraper.get_profile_data(profile_url)
#     print(data)
