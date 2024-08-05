from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import time

# load username and password
config = dotenv_values(".env")

# use selenium to start the browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://assetstore.unity.com/?q=vr%20free&orderBy=1")

try:
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".QVMvL"))
    )
    dropdown_button.click()

    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div/div[3]/span/div/div/div[2]/div[2]"))
    )
    login_button.click()
except Exception as e:
    print(f"Error finding login button: {e}")
    driver.quit()
    exit()

# Login
try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'conversations_create_session_form_email'))
    )
    password = driver.find_element(By.ID, "conversations_create_session_form_password")

    username.send_keys(config["UNITY_USERNAME"])
    password.send_keys(config["UNITY_PASSWORD"])

    login_submit = driver.find_element(By.XPATH, "/html/body/div[1]/section/div/div/div/div/form/div[2]/div[2]/div/div[1]/div/div[1]/input")
    login_submit.click()
except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()
    exit()

time.sleep(3)

assets = driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to My Assets')]")

for asset in assets:
    try:
        print(asset)
    except Exception as e:
        print(f"Error processing asset: {e}")
        continue



""" 
# parse the page
soup = BeautifulSoup(driver.page_source, 'html.parser')

free_asset_toggle = soup.find('div', string='Pricing')
if free_asset_toggle:
    print("located toggle button", free_asset_toggle)
else:
    print('not working')
    driver.quit()
"""
driver.quit()
