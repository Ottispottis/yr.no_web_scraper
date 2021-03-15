from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd

URL = "https://www.yr.no/en"
PATH = "S:\pythonstuff\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)
driver.get(URL)
temps = []
max_temps = []

SEARCH_BTN = driver.find_element_by_xpath('//*[@id="page-header__search-button"]')
SEARCH_BTN.click()

SEARCH_BOX = driver.find_element_by_xpath('//*[@id="page-header__search-input"]')

city = input("Type a city: ")

SEARCH_BOX.send_keys(city)
SEARCH_BOX.send_keys(Keys.ENTER)
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-list__item")))
SUGGESTED_CLICK = driver.find_element_by_class_name("search-results-list__item")
SUGGESTED_CLICK.click()

try:
    main = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "daily-weather-list__intervals"))
    )
    temperatures = main.find_elements_by_class_name("daily-weather-list-item")
    for temperature in temperatures:
        temperatures_i = temperature.find_element_by_class_name("min-max-temperature__max")
        temps.append(temperatures_i.text)

except:
    driver.quit()

for i, x in enumerate(temps):
    temps[i] = x.replace("°", '')

for i in range(0, len(temps)):
    temps[i] = int(temps[i])

info = {"Temperatures": temps}
df = pd.DataFrame(info)
print(df)

driver.quit()