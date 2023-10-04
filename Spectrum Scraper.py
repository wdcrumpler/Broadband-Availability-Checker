import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data = pd.read_csv('addressesSpectrum.csv')
data['Eligible (Spectrum)'] = ''
data['Has Account (Spectrum)'] = ''
data['Need Unit Number (Spectrum)'] = ''
data['No Service (Spectrum)'] = ''
data['Need to Verify (Spectrum)']=''
data['Unknown (Spectrum)']=''

# Set up Selenium Chrome driver
chrome_options = Options()
#chrome_options.add_argument('--headless')
service = Service('C:\Program Files\Chrome Driver\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)


for index, row in data.iterrows():
    address = row['Address']
    zipcode = row['ZipCode']

# Load Spectrum website
    driver.get('https://www.spectrum.com/internet')

#Find and fill the address and zip fields, then submit the form
    addressInputArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="sp-localization-input address-input" and @name="address"]')))
    address_field = addressInputArray[0]
    driver.execute_script("arguments[0].value = arguments[1];", address_field, address)
    
    zipInputArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="sp-localization-input zip-input" and @name="zip"]')))
    zip_field = zipInputArray[0]
    driver.execute_script("arguments[0].value = arguments[1];", zip_field, zipcode)
    
    time.sleep(3)
    submitButtonArray = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Go')]")))
    submit_button =  submitButtonArray[0]
    driver.execute_script("arguments[0].click();", submit_button)
    
    # Wait for page to load, then grab page source
    time.sleep(3)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    #content = driver.page_source 
    url = driver.current_url
    while "localization?" in url:
        time.sleep(1)
        url = driver.current_url
    #print("Current url is",url)

# Update spreadsheet according to the content found on the page.
    if "buy/featured" in url:
        data.at[index, 'Eligible (Spectrum)'] = 'X'
        print("Eligible (Spectrum) set to X for",address)
    elif "house-not-found" in url:
        data.at[index, 'No Service (Spectrum)'] = 'X'
        print("No Service (Spectrum) set to X for",address)
    elif "address/out-of-footprint" in url:
        data.at[index, 'No Service (Spectrum)'] = 'X'
        print("No Service (Spectrum) set to X for",address)
    elif "address/buyflow-ineligible" in url:
        data.at[index, 'No Service (Spectrum)'] = 'X'
        print("No Service (Spectrum) set to X for",address)
    elif "required-apt" in url:
        data.at[index, 'Need Unit Number (Spectrum)'] = 'X'
        print("Need Unit Number (Spectrum) set to X for",address)
    elif "existing-coverage" in url:
        data.at[index, 'Has Account (Spectrum)'] = 'X'
        print("Has Account (Spectrum) set to X for",address)
    else:
        data.at[index, 'Unknown (Spectrum)'] = 'X'
        print("Unknown (Spectrum) set to X for",address)
    time.sleep(2)

# Save the updated DataFrame back to the CSV file and quit the driver
data.to_csv('addresses_with_info_Spectrum.csv', index=False)  
driver.quit()

print("CSV file updated successfully.")