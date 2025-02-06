# scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def login_and_scrape(org_code, user_id, password):
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
    driver.get('https://web.classplusapp.com/login')

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
    driver.quit()

    # Extract all video and PDF URLs
    video_urls = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]
    pdf_urls = [a['href'] for a in soup.find_all('a', href=True) if 'pdf' in a['href']]

    return video_urls, pdf_urls
