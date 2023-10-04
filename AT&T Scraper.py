import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx import Document

data = pd.read_csv('addressesAT&T.csv')
data['Eligible (AT&T)'] = ''
data['Has Account (AT&T)'] = ''
data['Need Unit Number (AT&T)'] = ''
data['No Service (AT&T)'] = ''
data['Unknown (AT&T)']=''

# Set up Selenium Chrome driver
chrome_options = Options()
#chrome_options.add_argument('--headless')
service = Service('C:\Program Files\Chrome Driver\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

for index, row in data.iterrows():
    address = row['Address']
    zipcode = row['ZipCode']
    fullAddress = row['Full Address']

# Load Spectrum website
    driver.get('https://www.xfinity.com/overview')

#Find and fill the address and zip fields, then submit the form
    print("Full address is",fullAddress)
    time.sleep(2)

    fullAddressInputArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="input text contained sc-prism-input-default" and @name="localizationAddressField"]')))
    full_address_field = fullAddressInputArray[0]
    driver.execute_script("arguments[0].value = arguments[1];", full_address_field, fullAddress)

    time.sleep(2)

    submitButtonArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Check availability')]")))
    submit_button =  submitButtonArray[0]
    driver.execute_script("arguments[0].click();", submit_button)
    print ("button pressed")

    time.sleep(3)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    url = driver.current_url

    if "active-address" in url:
        data.at[index, 'Has Account (Xfinity)'] = 'X'
        print("Has Account set to X for",address)
    elif "broadband/not-available" in url:
        data.at[index, 'No Service (Xfinity)'] = 'X'
        print("No Service set to X for",address)
    elif "buy/broadband/offers" in url:
        data.at[index, 'Eligible (Xfinity)'] = 'X'
        print("Eligible set to X for",address)
    elif "internet/hypergig-available" in url:
        data.at[index, 'Eligible (Xfinity)'] = 'X'
        print("Eligible set to X for",address)
    #elif "mdu-fallback-container__button-container" in content:
    elif '<h2 class="localization-container__header">Is one of these the correct address?</h2>' in content:
        data.at[index, 'Need Unit Number (Xfinity)'] = 'X'
        print("Need Unit Number set to X for",address)
    else:
        data.at[index, 'Unknown (Spectrum)'] = 'X'
        print("Unknown set to X for",address)
    
    time.sleep(6)
    driver.quit()
# Save the updated DataFrame back to the CSV file and quit the driver
data.to_csv('addresses_with_info_Spectrum.csv', index=False)  
driver.quit()

print("CSV file updated successfully.")