import asyncio
from playwright.async_api import async_playwright
import json
import os
import random

# Keywords that will be used to search for links
PRIVACY_POLICY_KEYWORDS = ['privacy policy', 'privacy']
DNSMPI_KEYWORDS = ['DNSMPI', 'do not share', 'sell my personal information', 'Share My Personal Data']

# Get the directory of the current file
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Navigate to the data folder from the current file's directory
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, '..', 'data') 
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Fetch the links from a website based on the keywords
async def fetch_link(page, keywords, use_xpath=False):
    # Prepare CSS selectors based on keywords
    selectors = [f'a:has-text("{keyword}")' for keyword in keywords]
    
    # Include XPath selector as an option
    if use_xpath:
        selectors += [f'//a[contains(text(), "{keyword}")]' for keyword in keywords]

    # Iterator over the selectors to find visible link
    for selector in selectors:
        try:
            # Locate the element
            element = page.locator(selector).first
            if await element.is_visible():
                # Extract the href attribute
                link = await element.get_attribute('href')
                if link:
                    return link
        except Exception as e:
            print(f"Error locating element for keyword '{selector}': {e}")
    return None

# Scrape a website to find the desired links 
async def scrape_website(browser, url, retries=3):

    # Ensure url is formatted correctly
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Scrape the privacy policy and the DNSMPI content from website
    # Create the new browser context and page 
    context = await browser.new_context()
    page = await context.new_page()

    try:
        # timeout is set to 30 seconds
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state('domcontentloaded')

        # Scrape the Priacy Policy link
        privacy_content = await fetch_link(page, PRIVACY_POLICY_KEYWORDS)

        # If the link is relative, append to the base url
        if privacy_content and not privacy_content.startswith('http'):
            privacy_content = url.rstrip('/') + privacy_content

        # Scrape the DNSMPI Link
        dnsmpi_content = await fetch_link(page, DNSMPI_KEYWORDS)
        
        # If the link is relative, append to the base url
        if dnsmpi_content and not dnsmpi_content.startswith("http"):
            dnsmpi_content = url.rstrip("/") + dnsmpi_content

        # Create a dictionary to store results
        result = {
            'url': url,
            'privacy_policy': privacy_content if privacy_content else "Not Found",
            'dnsmpi': dnsmpi_content if dnsmpi_content else "Not Found"
        }

        # Save the results in JSON file
        safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        filepath = os.path.join(OUTPUT_DIRECTORY, f'{safe_filename}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        print(f'Scrapped data saved for {url}')

    except Exception as e:
        # Retry scraping on failure
        if retries > 0:
            print(f'Retrying {url}, attempts left: {retries}')
            await scrape_website(browser, url, retries - 1)
        else:
            print(f'Failed to scrape {url}: {e}')
    finally:
        await page.close()

# Random delay between 3 and 8 seconds to help with rate limiting
async def scrape_website_with_delay(browser, url):
    await asyncio.sleep(random.uniform(3,8))
    await scrape_website(browser, url)

# Main to run the crawler
async def main(urls):
    async with async_playwright() as playwright:
        # Launch the browser in headless mode
        browser = await playwright.chromium.launch(headless=True)

        # Creates list of tasks to fetch content from each url
        tasks = [scrape_website_with_delay(browser, url) for url in urls]
        # asyncio.gather to run all of the task concurrently(all at same time)
        await asyncio.gather(*tasks)

        await browser.close()

# Entry Point 
if __name__ == "__main__":
    urls = [
    'https://books.toscrape.com/',
    'https://quotes.toscrape.com/',
    'https://scrapethissite.com/',
    'https://crawler-test.com/',
    'https://httpbin.org/',
    'https://the-internet.herokuapp.com/',
    'https://jsonplaceholder.typicode.com/',
    'https://realpython.github.io/fake-jobs/',
    'https://s1.demo.opensourcecms.com/wordpress/',
    'https://www.google.com/',
    'https://www.mlb.com/',
    'https://www.pga.com/',
    'https://www.nba.com/',
    'https://www.amazon.com/',
    'https://www.ebay.com/',
    'https://www.wikipedia.org/',
    'https://www.bbc.com/',
    'https://www.nytimes.com/',
    'https://www.cnn.com/',
    'https://www.microsoft.com/',
    'https://www.apple.com/'
    ]

    asyncio.run(main(urls))
