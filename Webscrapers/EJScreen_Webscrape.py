import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
import json
import time
api_url = "https://ejscreen.epa.gov/mapper/ejscreenapi.html"
services = ["C:/DevTools/Drivers/geckodriver-v0.31.0-win64/geckodriver.exe", 
            "C:/DevTools/Drivers/chromedriver_win32/chromedriver.exe",
            "C:/DevTools/Drivers/edgedriver_win64/msedgedriver.exe"]  #Add more if necessary (consider making the driver selection dynamic)

def recurBrowser(numTry):
    try:
        s = Service(services[numTry])
        if (numTry == 0):
            driver = webdriver.Firefox(service=s)
        elif (numTry == 1):
            driver = webdriver.Chrome(service=s)
        else:
            driver = webdriver.Edge(service=s)
        return driver
    except Exception as e:
        numTry += 1
        print(e)
        if (numTry == len(services)):
            print("No browsers worked...exiting")
            exit(1)
        tryBrowser(numTry)

def tryBrowser():
    return recurBrowser(0)

#Make sure the page is up
page = requests.get(api_url)
if (page.status_code != 200):
    print("API Webpage down or not found...")
    exit(1)




#Driver gets webpage
driver = tryBrowser()
driver.get(api_url)

#Find and click county button
time.sleep(5)
countyButton = driver.find_element(By.XPATH, "//input[@type='radio'][@name='inmethod'][@value='county']")
countyButton.click()

#Find textbox and enter county FIPS code(s)
time.sleep(5)
textBox = driver.find_element(By.XPATH, "//input[@type='text'][@name='areaid']")
textBox.send_keys("42001")
textBox.send_keys(Keys.RETURN)

#Extract json content
time.sleep(7)
content = driver.find_element(By.ID, "resultjson").text
parsed_json = json.loads(content)
print(parsed_json)

driver.close()
exit(1)