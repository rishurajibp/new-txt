# scraper.py

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
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

    # Set up the Selenium WebDriver with ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    try:
        logger.info("Initializing ChromeDriver...")
        driver = webdriver.Chrome(options=options)

        # Navigate to the login page
        logger.info("Navigating to the login page...")
        driver.get('https://example.com/login')

        # Perform login
        logger.info("Logging in with provided credentials...")
        org_code_field = driver.find_element(By.NAME, 'org_code')
        user_id_field = driver.find_element(By.NAME, 'user_id')
        password_field = driver.find_element(By.NAME, 'password')

        org_code_field.send_keys(org_code)
        user_id_field.send_keys(user_id)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to load after login
        logger.info("Waiting for the page to load...")
        time.sleep(5)

        # Get the page source and parse it with BeautifulSoup
        logger.info("Parsing the page source...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract all video and PDF URLs
        logger.info("Extracting video and PDF URLs...")
        video_urls = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]
        pdf_urls = [a['href'] for a in soup.find_all('a', href=True) if 'pdf' in a['href']]

        logger.info(f"Found {len(video_urls)} video URLs and {len(pdf_urls)} PDF URLs.")
        return video_urls, pdf_urls

    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
        raise

    finally:
        logger.info("Closing the browser...")
        driver.quit()
