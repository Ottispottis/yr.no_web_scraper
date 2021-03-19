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
#driver = webdriver.Chrome(PATH, options=options)
driver = webdriver.Chrome(PATH)
driver.get(URL)
temps = []
max_temps = []
min_temps = []
average = []
dates = []

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
        max_temps.append(temperatures_i.text)
    for temperature_min in temperatures:
        temperature_j = temperature_min.find_element_by_class_name("min-max-temperature__min")
        min_temps.append(temperature_j.text)
    for date in temperatures:
        dates_i = date.find_element_by_class_name("date-label")
        dates.append(dates_i.text)

except:
    driver.quit()

for i, x in enumerate(max_temps):
    max_temps[i] = x.replace("°", '')

for i, x in enumerate(min_temps):
    min_temps[i] = x.replace("°", '')

for i in range(0, len(max_temps)):
    max_temps[i] = int(max_temps[i])

for i in range(0, len(min_temps)):
    min_temps[i] = int(min_temps[i])

sum_list = [i + j for (i, j) in zip(max_temps, min_temps)]

for i in range(len(sum_list)):
    average.append(sum_list[i]/2)


info = {"Date": dates, "Max temp": max_temps, "Min temp": min_temps, "Average": average}
df = pd.DataFrame(info)
print(df)
df.to_csv("data.csv")
driver.quit()
