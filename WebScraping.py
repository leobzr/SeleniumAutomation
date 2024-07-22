from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

# Define the path to your chromedriver
chromedriver_path = "chromedriver.exe"

# Create a ChromeOptions object and add the incognito argument
driver_options = webdriver.ChromeOptions()
driver_options.add_argument("--incognito")

# Define a function to create a webdriver instance
def create_webdriver():
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=driver_options)

try:
    # Open the website
    browser = create_webdriver()
    browser.get("https://github.com/collections/machine-learning")

    # Wait until the desired element is present (modify as needed)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

    # Perform your actions on the website here
    print("Website loaded successfully.")

except TimeoutException:
    print("Timed out waiting for page to load.")
except Exception as e:
    print(f"An error occurred: {e}")

# Extract all projects:
projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")

# Extract information for each project
project_list = {}
for proj in projects:
    proj_name = proj.text
    proj_url = proj.find_element(By.XPATH, "a").get_attribute('href')
    project_list[proj_name] = proj_url

# Close the browser
browser.quit()

# Extracting data
project_df = pd.DataFrame.from_dict(project_list, orient='index', columns=['URL'])
print(project_df)
