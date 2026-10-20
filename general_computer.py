#open and execute another file
"""
with open("test boundaries/file.py") as file:
  exec(file.read())
"""



"""
import requests
url = "https://vocafy.ch"
response = requests.get(url)

if response.status_code == 200:
  print(response.text)
else:
  print("failed")
"""








"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client


account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = "+16466635422"
target_number = "+41795350603"

client = Client(account_sid, auth_token)

options = Options()
options.add_argument("--headless")

previous_state = {}

while True:
    for i in range(3001, 3020):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            Link = "http://83.77.148.163:" + str(i) + "/"
            driver.get(Link)
            current_state = "Online"
        except Exception as e:
            current_state = "Offline"
        finally: 
          if driver: 
            driver.quit()

        if i not in previous_state or previous_state[i] != current_state:
            message = client.messages.create(
                body=f"{Link} is {current_state}",
                from_=twilio_number,
                to=target_number     
            )
            previous_state[i] = current_state
            
    time.sleep(900)
"""


import subprocess
from selenium import webdriver
#subprocess.run(["C:\\Program Files\\Mozilla Firefox\\firefox.exe"])

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client

options = Options()
options.add_argument("--start-minimized")  # Optional: Opens the browser in fullscreen
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://google.com")

cookies_button = driver.find_element(By.ID, "L2AGLb")
if cookies_button:
  cookies_button.click()

search_bar = driver.find_element(By.NAME, "q")
search_term = "how to automate a computer by using python"
set_search_term = ""

for char in search_term:
  search_bar.send_keys(char)
  time.sleep(0.01)

search_bar.send_keys(Keys.RETURN)

first_result = driver.find_element(By.XPATH, "//h3/ancestor::a")
first_result.click()


driver.back()
time.sleep(1)
driver.back()