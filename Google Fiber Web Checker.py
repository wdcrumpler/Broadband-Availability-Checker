import time
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from docx import Document

def fetch_page_content(url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    return driver.page_source

def parse_content(content):
    return BeautifulSoup(content, 'html.parser')

# Read data from the CSV file into a pandas DataFrame and initialize columns
data = pd.read_csv('addresses.csv')
data['Eligible (GF)'] = ''
data['Has Account (GF)'] = ''
data['Need Unit Number (GF)'] = ''
data['No Service (GF)'] = ''
data['Unknown (GF)']=''

url = 'https://fiber.google.com/db/'

# Set up Selenium Chrome driver
chrome_options = Options()
chrome_options.add_argument('--headless')
service = Service('C:\Program Files\Chrome Driver\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

for index, row in data.iterrows():
    address = row['Address']
    zipcode = row['ZipCode']
    
# Load Google Fiber website
    driver.get('https://fiber.google.com/db/')

# Find and fill the address and zip fields, then submit the form
    addressInputArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="mdc-text-field__input" and @name="street"]')))
    address_field = addressInputArray[1]
    driver.execute_script("arguments[0].value = arguments[1];", address_field, address)
    
    zipInputArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="mdc-text-field__input" and @name="zip"]')))
    zip_field = zipInputArray[1]
    driver.execute_script("arguments[0].value = arguments[1];", zip_field, zipcode)
    
    time.sleep(10)
    submitButtonArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Check availability')]")))
    submit_button =  submitButtonArray[3]
    driver.execute_script("arguments[0].click();", submit_button)
    
    # Wait for page to load, then grab page source
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    content = driver.page_source

    # Update spreadsheet according to the content found on the page.
    if "You’re eligible to get Google Fiber Internet." in content:
        data.at[index, 'Eligible (GF)'] = 'X'
        print("Eligible set to X for",address)
    elif "INELIGIBLE address-status__container address-status__container--visible" in content:
        data.at[index, 'No Service (GF)'] = 'X'
        print("No Service set to X for",address)
    elif "UNIT_NUMBER_MISSING address-status__container address-status__container--visible" in content:
        data.at[index, 'Need Unit Number (GF)'] = 'X'
        print("Need Unit Number set to X for",address)
    elif "This address has a Google Fiber account" in content:
        data.at[index, 'Has Account (GF)'] = 'X'
        print("Has Account set to X for",address)
    else:
        data.at[index, 'Unknown (GF)'] = 'X'
        print("Unknown set to X for",address)
    time.sleep(10)

# Save the updated DataFrame back to the CSV file and quit the driver
data.to_csv('addresses_with_info.csv', index=False)  
driver.quit()

print("CSV file updated successfully.")