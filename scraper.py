# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def login_and_scrape(org_code, user_id, password):
    # Set up the Selenium WebDriver with ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # Disable sandboxing for Linux

    # Specify the path to ChromeDriver (if not in PATH)
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)

    try:
        # Navigate to the login page
        driver.get('https://example.com/login')

        # Perform login
        org_code_field = driver.find_element(By.NAME, 'org_code')
        user_id_field = driver.find_element(By.NAME, 'user_id')
        password_field = driver.find_element(By.NAME, 'password')

        org_code_field.send_keys(org_code)
        user_id_field.send_keys(user_id)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to load after login
        time.sleep(5)

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract all video and PDF URLs
        video_urls = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]
        pdf_urls = [a['href'] for a in soup.find_all('a', href=True) if 'pdf' in a['href']]

        return video_urls, pdf_urls

    finally:
        # Close the browser
        driver.quit()
    video_urls = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]
    pdf_urls = [a['href'] for a in soup.find_all('a', href=True) if 'pdf' in a['href']]

    return video_urls, pdf_urls
