import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Load the Google Sheet as a pandas dataframe
df = pd.read_csv('Web Scraping Assignment.csv')

# Create a new dataframe to store the results
results = pd.DataFrame(columns=['College', 'Address'])

# Configure the Selenium webdriver to run in headless mode
browser= webdriver.Chrome(executable_path='D:\freelancing\chromedriver.exe')
chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)
print(df.columns)
# Loop through each row in the dataframe

for index, row in df.iterrows():
    website = row[' WEBSITE']
    if pd.notna(website):
        try:
            response = requests.get(website, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            driver.find_element(By.PARTIAL_LINK_TEXT,'Con').click()
            address_tag = soup.find_all('single-con-add-text', 'div')
            if len(address_tag) > 0:
                address = address_tag[0].get_text().strip()
                df.at[index, 'Address'] = address
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print(f"Could not connect to {website}")
        except Exception as e:
            print(f"An error occurred while accessing {website}: {e}")


df.to_csv('colleges_with_address.csv', index=False)

# Close the Selenium webdriver
driver.quit()

# Save the results to a new CSV file
# results.to_csv('college_addresses.csv', index=False)
