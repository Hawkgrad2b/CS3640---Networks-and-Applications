import asyncio
from playwright.async_api import async_playwright
import json
import os
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import textstat
from bs4.element import Comment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Keywords for finding privacy policy and DNSMPI links
PRIVACY_POLICY_KEYWORDS = [
    'privacy policy', 'Privacy', 'cookie policy', 'New Privacy Policy', 'legal privacy', 'data protection'
]
DNSMPI_KEYWORDS = [
    'DNSMPI', 'do not share', 'sell my personal information', 'Share My Personal Data',
    'Do not sell or share my personal information'
]

# Base directory and output folder
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, '..', 'data')
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Function to dynamically build XPath selectors
def build_xpath_selectors(keywords):
    selectors = []
    for keyword in keywords:
        selectors.extend([
            f'//a[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{keyword.lower()}")]',
            f'//a[contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{keyword.lower()}")]',
            f'//a[contains(translate(@id, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{keyword.lower()}")]',
            f'//a[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{keyword.lower()}")]',
            f'//a[@role="link" and contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{keyword.lower()}")]',
        ])
    return selectors

# Function to fetch the link from a website based on the keywords
async def fetch_link(page, keywords):
    selectors = build_xpath_selectors(keywords)
    for selector in selectors:
        try:
            element = await page.query_selector(selector)
            if element:
                href = await element.get_attribute('href')
                if href:
                    return urljoin(page.url, href)
        except Exception:
            continue
    return None

# Helper function to filter visible text
def tag_visible(element):
    if isinstance(element, Comment):
        return False
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]', 'noscript']:
        return False
    return True

# Function to analyze clarity of the privacy policy
def analyze_clarity(policy_url):
    try:
        response = requests.get(policy_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract visible text
        texts = soup.find_all(text=True)
        visible_texts = filter(tag_visible, texts)
        text = u" ".join(t.strip() for t in visible_texts)

        # Calculate readability scores
        fk_grade = textstat.flesch_kincaid_grade(text)
        fre_score = textstat.flesch_reading_ease(text)

        # Record results
        result = {
            'flesch_kincaid_grade': fk_grade,
            'flesch_reading_ease': fre_score
        }
        return result
    except Exception as e:
        logger.error(f"Error analyzing clarity for {policy_url}: {e}")
        return {
            'flesch_kincaid_grade': None,
            'flesch_reading_ease': None
        }

async def assess_accessibility(page, link_keywords):
    accessible = False
    clicks_required = None  # Initialize to None
    link_href = None

    # Try to find the link on the homepage
    link_href = await fetch_link(page, link_keywords)
    if link_href:
        accessible = True
        clicks_required = 0  # Found on homepage
    else:
        # Try navigating through clickable elements (simulate up to two clicks)
        max_clicks = 2
        for clicks in range(1, max_clicks + 1):
            clickable_elements = await page.query_selector_all('a')
            for element in clickable_elements:
                try:
                    await element.click(timeout=2000)
                    link_href = await fetch_link(page, link_keywords)
                    if link_href:
                        accessible = True
                        clicks_required = clicks  # Set clicks_required here
                        break
                    await page.go_back()
                except Exception:
                    continue
            if accessible:
                break
    return link_href, accessible, clicks_required

# Function to monitor JavaScript fingerprinting-related activity
async def monitor_fingerprinting(page):
    fingerprinting_data = {
        "canvas_calls": 0,
        "webgl_calls": 0,
        "navigator_properties": [],
        "external_fingerprinting_libraries": [],
    }

    async def intercept_requests(route):
        url = route.request.url
        if any(x in url for x in ["fingerprintjs", "fpjs", "evercookie"]):
            fingerprinting_data["external_fingerprinting_libraries"].append(url)
        await route.continue_()

    page.on("request", intercept_requests)

    # Check for Canvas and WebGL API usage
    await page.expose_function("interceptCanvas", lambda: fingerprinting_data.update({"canvas_calls": fingerprinting_data["canvas_calls"] + 1}))
    await page.expose_function("interceptWebGL", lambda: fingerprinting_data.update({"webgl_calls": fingerprinting_data["webgl_calls"] + 1}))
    
    await page.add_init_script("""
        const originalCanvasToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {
            window.interceptCanvas();
            return originalCanvasToDataURL.apply(this, arguments);
        };

        const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function() {
            window.interceptWebGL();
            return originalGetParameter.apply(this, arguments);
        };
    """)

    return fingerprinting_data

# Enhanced scrape_website function
async def scrape_website(browser, url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    page = await browser.new_page()

    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state('domcontentloaded')

        # Assess accessibility for Privacy Policy link
        privacy_link, privacy_accessible, privacy_clicks = await assess_accessibility(page, PRIVACY_POLICY_KEYWORDS)

        # Assess accessibility for DNSMPI link
        dnsmpi_link, dnsmpi_accessible, dnsmpi_clicks = await assess_accessibility(page, DNSMPI_KEYWORDS)

        # Analyze clarity if privacy policy link is found
        if privacy_link:
            clarity_result = analyze_clarity(privacy_link)
        else:
            clarity_result = {
                'flesch_kincaid_grade': None,
                'flesch_reading_ease': None
            }

        # Monitor fingerprinting
        fingerprinting_data = await monitor_fingerprinting(page)

        # Build the result dictionary
        result = {
            'url': url,
            'privacy_policy': {
                'link': privacy_link if privacy_link else "Not Found",
                'accessible_within_two_clicks': privacy_accessible,
                'clicks_required': privacy_clicks if privacy_accessible else None,
                'flesch_kincaid_grade': clarity_result.get('flesch_kincaid_grade'),
                'flesch_reading_ease': clarity_result.get('flesch_reading_ease')
            },
            'dnsmpi': {
                'link': dnsmpi_link if dnsmpi_link else "Not Found",
                'accessible_within_two_clicks': dnsmpi_accessible,
                'clicks_required': dnsmpi_clicks if dnsmpi_accessible else None
            },
            'fingerprinting': fingerprinting_data
        }

        # Save results in a JSON file
        safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        filepath = os.path.join(OUTPUT_DIRECTORY, f'{safe_filename}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        logger.info(f'Successfully scraped: {url}')

    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")

    finally:
        await page.close()

# Main function
async def main(urls):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        tasks = [scrape_website(browser, url) for url in urls]
        await asyncio.gather(*tasks)
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

