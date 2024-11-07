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
                page.goto("https://www.linkedin.com/login")
                page.fill("#username", username)
                page.fill("#password", password)
                page.click('button[type="submit"]')
                page.wait_for_load_state("domcontentloaded")

                # Check if login failed
                if "login" in page.url:
                    logger.error("Login failed")
                    raise Exception("Login failed")

                logger.info("Login successful, going to profile page")

                # Go to profile page
                page.goto(profile_url)
                page.wait_for_load_state("domcontentloaded")

                # Get profile data
                name = page.text_content(".text-heading-xlarge")
                headline = page.text_content(".text-body-medium")

                if not name or not headline:
                    raise Exception("Failed to fetch name or headline from profile.")

                logger.info(f"Scraped profile: {name} - {headline}")

                logger.info("Going to recent post page")
                feeds_url = f"{profile_url}/recent-activity/all/"

                # Go to feeds page
                page.goto(feeds_url)
                page.wait_for_load_state("domcontentloaded")

                posts = []
                page.wait_for_selector(".feed-shared-update-v2", timeout=10000)
                post_elements = page.query_selector_all(".feed-shared-update-v2")

                if not len(post_elements):
                    logger.warning("No posts found")

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
                return {
                    "name": name.strip(),
                    "headline": headline.strip(),
                    "posts": posts,
                }

            except Exception as e:
                print(e)
                # logger.error(f"Error scraping profile: {str(e)}")
                return {
                    "name": "Failed to fetch",
                    "headline": "Failed to fetch",
                    "posts": [],
                }
            finally:
                browser.close()


# if __name__ == "__main__":
#     scraper = LinkedInScraper()
#     username = os.getenv("LINKEDIN_USERNAME")
#     password = os.getenv("LINKEDIN_PASSWORD")
#     profile_url = "https://www.linkedin.com/in/aniket-bajpai"

#     data = scraper.get_profile_data(username, password, profile_url)
#     print(data)
