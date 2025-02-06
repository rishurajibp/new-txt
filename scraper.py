# scraper.py

import logging
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def login_and_scrape(org_code, user_id, password):
    logger.info("Starting web scraping process...")

    # Create a session to persist cookies
    session = requests.Session()

    # Perform login
    login_url = 'https://example.com/login'
    login_data = {
        'org_code': org_code,
        'user_id': user_id,
        'password': password
    }

    try:
        logger.info("Logging in to the website...")
        response = session.post(login_url, data=login_data)
        response.raise_for_status()  # Raise an error for bad status codes

        # Check if login was successful
        if "Login Failed" in response.text:
            logger.error("Login failed. Check your credentials.")
            raise Exception("Login failed. Check your credentials.")

        logger.info("Login successful. Scraping the website...")

        # Scrape the page for video and PDF URLs
        target_url = 'https://example.com/dashboard'  # Replace with the actual target page
        response = session.get(target_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all video and PDF URLs
        video_urls = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]
        pdf_urls = [a['href'] for a in soup.find_all('a', href=True) if 'pdf' in a['href']]

        logger.info(f"Found {len(video_urls)} video URLs and {len(pdf_urls)} PDF URLs.")
        return video_urls, pdf_urls

    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
        raise
