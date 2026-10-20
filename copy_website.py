from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

url = "https://vocafy.ch"

# Fetch the page content with requests
response = requests.get(url)

if response.status_code == 200:
    print("Page fetched successfully.")

    # Initialize WebDriver service
    service = Service(ChromeDriverManager().install())

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)

    # Open the driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Wait for the body or the specific element to be fully loaded
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for body to load

    # Open the page using Selenium
    driver.get(url)

    try:
        # Wait for the element with the specific class to be present

        # Find the first element by class name (use an alternative locator if necessary)
        element = driver.find_element(By.CLASS_NAME, "headLeftConP")

        inline_style = element.get_attribute('style')
        print(f"Inline Style: {inline_style}")

    except Exception as e:
        print(f"Error: {e}")

    # Quit the driver after usage
    driver.quit()
else:
    print("Failed to fetch the page.")
