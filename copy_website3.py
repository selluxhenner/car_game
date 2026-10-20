from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to open
url = 'http://tiger-wil.ch'  # Replace with your target URL
driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))

# Get the page source HTML after all elements are loaded
page_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all elements in the HTML and filter to the first 10 with `id` or `class`
elements = [el for el in soup.find_all(True) if el.has_attr("id") or el.has_attr("class")][:10]

# List to store HTML and CSS of each element
element_data = []

# Process each filtered element
for element in elements:
    # Get HTML code for the element
    element_html = str(element)
    selenium_element = None

    # Attempt to locate the element in Selenium by `id` or `class`
    if element.has_attr("id"):
        selenium_element = driver.find_element(By.ID, element["id"])
    elif element.has_attr("class"):
        class_name = " ".join(element["class"])  # Join class list into a single string
        selenium_element = driver.find_element(By.CLASS_NAME, class_name.split()[0])  # Use the first class for location

    # If the element was successfully found
    if selenium_element:
        # Get computed CSS styles
        styles = driver.execute_script(
            """
            let element = arguments[0];
            let computedStyles = window.getComputedStyle(element);
            let styleObj = {};
            for (let i = 0; i < computedStyles.length; i++) {
                let property = computedStyles[i];
                styleObj[property] = computedStyles.getPropertyValue(property);
            }
            return styleObj;
            """,
            selenium_element
        )

        # Store HTML and styles in a dictionary
        element_data.append({
            "html": element_html,
            "styles": styles
        })

# Print the HTML and styles for each element
for idx, data in enumerate(element_data):
    print(f"\nElement {idx + 1}:")
    print("HTML:", data["html"])
    print("Styles:")
    for prop, val in data["styles"].items():
        print(f"  {prop}: {val}")

# Close the driver
driver.quit()
