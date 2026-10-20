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

# Find all elements in the HTML
elements = soup.find_all(True)  # Get every element in the HTML

# List to store HTML and CSS of each element
element_data = []

# Process each element
for element in elements:
    # Get HTML code for the element
    element_html = str(element)
    selenium_element = None

    # Attempt to locate the element in Selenium by `id` or `class` (if present)
    if element.has_attr("id"):
        selenium_element = driver.find_element(By.ID, element["id"])
    elif element.has_attr("class"):
        class_name = " ".join(element["class"])  # Join class list into a single string
        selenium_element = driver.find_element(By.CLASS_NAME, class_name.split()[0])  # Use the first class for location
    else:
        # Fallback for elements without id or class (locate by tag name)
        tag_name = element.name
        selenium_element = driver.find_element(By.TAG_NAME, tag_name)

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

        # Remove styles starting with "-" (vendor-specific)
        styles = {prop: val for prop, val in styles.items() if not prop.startswith("-")}

        # Store HTML and filtered styles in a dictionary
        element_data.append({
            "html": element_html,
            "styles": styles
        })

# Build the new HTML content
new_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracted Website</title>
    <style>
"""

# Add relevant styles to the new HTML
for idx, data in enumerate(element_data):
    for prop, val in data["styles"].items():
        new_html += f"        {prop}: {val};\n"

new_html += """
    </style>
</head>
<body>
"""

# Add the filtered HTML elements
for idx, data in enumerate(element_data):
    new_html += f"\n    <!-- Element {idx + 1} -->\n"
    new_html += f"    {data['html']}\n"

# Close the body and HTML tags
new_html += """
</body>
</html>
"""

# Write the new HTML content to a file
output_file = "extracted_website.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(new_html)

# Print the path to the new HTML file
print(f"New HTML file created: {output_file}")

# Close the driver
driver.quit()
