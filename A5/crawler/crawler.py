import asyncio
from playwright.async_api import async_playwright
import json
import os
import random
import logging
import traceback
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Keywords for finding privacy policy links
PRIVACY_POLICY_KEYWORDS = ['privacy policy', 'Privacy', 'cookie policy', 'privacy policy', 'New Privacy Policy', 'legal privacy', 'data protection']
DNSMPI_KEYWORDS = ['DNSMPI', 'do not share', 'sell my personal information', 'Share My Personal Data', 'Do not sell or share my personal information']

# Base directory and output folder
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, '..', 'data')
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Function to dynamically build XPath selectors
def build_xpath_selectors(keywords):
    selectors = []
    for keyword in keywords:
         selectors.extend([
            f'//a[contains(text(), "{keyword}")]',                    # Text-based
            f'//a[contains(@aria-label, "{keyword}")]',               # ARIA labels
            f'//a[contains(@data-omtr-intcmp, "{keyword}")]',         # Data-omtr-intcmp attributes
            f'//a[contains(@id, "{keyword.lower()}")]',               # ID-based
            f'//a[contains(@href, "{keyword.lower()}")]',             # HREF-based
            f'//a[@role="link" and contains(text(), "{keyword}")]',  # Role-based
        ])
    return selectors

# Refactored fetch_link function with prioritized selectors
async def fetch_link(page, keywords):
    # Search for a matching link based on CSS and XPath selectors.
    css_selectors = [f'a:has-text("{keyword}")' for keyword in keywords]
    xpath_selectors = build_xpath_selectors(keywords)
    all_selectors = css_selectors + xpath_selectors

    for selector in all_selectors:
        try:
            # Locate the element
            element = page.locator(selector).first
            if await element.is_visible():
                # Extract the href attribute
                link = await element.get_attribute('href')
                if link:
                    # Ensure absolute URL
                    if link.startswith("//"):
                        link = "https:" + link
                    elif link.startswith("/"):
                        link = urljoin(page.url, link)
                    return link
                
        except Exception as e:
            logger.debug(f"Selector '{selector}' failed: {e}")
    return None

# Enhanced error handling in scrape_website
async def scrape_website(browser, url, retries=3):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    context = await browser.new_context()
    page = await context.new_page()

    try:
        await page.goto(url, timeout=60000)  # Timeout set to 60 seconds
        await page.wait_for_load_state('domcontentloaded')

        privacy_link = await fetch_link(page, PRIVACY_POLICY_KEYWORDS)
        dnsmpi_link = await fetch_link(page, DNSMPI_KEYWORDS)

        # Build the result dictionary
        result = {
            'url': url,
            'privacy_policy': urljoin(url, privacy_link) if privacy_link else "Not Found",
            'dnsmpi': urljoin(url, dnsmpi_link) if dnsmpi_link else "Not Found",
        }

        # Save results in a JSON file
        safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        filepath = os.path.join(OUTPUT_DIRECTORY, f'{safe_filename}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        logger.info(f'Successfully scraped: {url}')

        if not privacy_link:
            logger.warning(f"No privacy policy found for {url}. Consider adding new patterns.")

    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")

    finally:
        await page.close()

# Random delay for rate limiting
async def scrape_website_with_delay(browser, url, min_delay=3, max_delay=8):
    await asyncio.sleep(random.uniform(min_delay, max_delay))
    await scrape_website(browser, url)

# Process URLs in batches
async def process_in_batches(browser, urls, batch_size=10):
    semaphore = asyncio.Semaphore(batch_size)

    async def sem_task(url):
        async with semaphore:
            await scrape_website_with_delay(browser, url)

    tasks = [sem_task(url) for url in urls]

    for i in range(0, len(tasks), batch_size):
        await asyncio.gather(*tasks[i:i + batch_size])

# Main function
async def main(urls):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, args=["--disable-http2"])
        await process_in_batches(browser, urls, batch_size=5)  # Reduced batch size for safer processing
        await browser.close()

# Example usage
if __name__ == "__main__":
    urls = [
  "google.com",
  "facebook.com",
  "instagram.com",
  "wikipedia.org",
  "yahoo.com",
  "reddit.com",
  "whatsapp.com",
  "amazon.com",
  "chatgpt.com",
  "tiktok.com",
  "bing.com",
  "pinterest.com",
  "twitter.com",
  "linkedin.com",
  "ebay.com",
  "microsoft.com",
  "netflix.com",
  "espn.com",
  "cnn.com",
  "foxnews.com",
  "bbc.com",
  "disneyplus.com",
  "spotify.com",
  "twitch.tv",
  "shopify.com",
  "apple.com",
  "adobe.com",
  "medium.com",
  "github.com",
  "stackexchange.com",
  "craigslist.org",
  "zoom.us",
  "indeed.com",
  "accuweather.com",
  "wordpress.com",
  "yelp.com",
  "homedepot.com",
  "patreon.com",
  "tumblr.com",
  "deviantart.com",
  "character.ai",
  "messenger.com",
  "snapchat.com",
  "outbrain.com",
  "fandom.com",
  "theguardian.com",
  "playstation.com",
  "capitalone.com",
  "figma.com",
  "canva.com",
  "deepl.com",
  "paypal.com",
  "booking.com",
  "imdb.com",
  "etsy.com",
  "zillow.com",
  "bbc.co.uk",
  "hulu.com",
  "target.com",
  "lowes.com",
  "wayfair.com",
  "walmart.com",
  "tripadvisor.com",
  "kohls.com",
  "macys.com",
  "nytimes.com",
  "usps.com",
  "weather.com",
  "forbes.com",
  "bloomberg.com",
  "reuters.com",
  "npr.org",
  "time.com",
  "theatlantic.com",
  "vox.com",
  "wired.com",
  "polygon.com",
  "kotaku.com",
  "sports.yahoo.com",
  "bleacherreport.com",
  "msnbc.com",
  "nbcnews.com",
  "abcnews.go.com",
  "cbsnews.com",
  "usatoday.com",
  "latimes.com",
  "chicagotribune.com",
  "sfgate.com",
  "houstonchronicle.com",
  "philly.com",
  "miamiherald.com",
  "boston.com",
  "detroitnews.com",
  "denverpost.com",
  "dallasnews.com",
  "startribune.com",
  "cleveland.com",
  "slate.com",
  "salon.com"
]
    asyncio.run(main(urls))

