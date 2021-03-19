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

#driver = webdriver.Chrome(PATH, options=options) #Disables chrome window.
driver = webdriver.Chrome(PATH)
driver.get(URL)

temps = []
max_temps = []
min_temps = []
average = []
dates = []
wind_speed = []
rain_amount = []
# Locating the search button on the web page and clicking on it

SEARCH_BTN = driver.find_element_by_xpath('//*[@id="page-header__search-button"]')
SEARCH_BTN.click()

# Locating the search box after clicking on the search button

SEARCH_BOX = driver.find_element_by_xpath('//*[@id="page-header__search-input"]')

city = input("Type a city: ")

# Sending user input to the web pages search bar.

SEARCH_BOX.send_keys(city)
SEARCH_BOX.send_keys(Keys.ENTER)

# Waiting for the page to load, continues when search-results-list__item is loaded.

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-list__item")))

# Click on the first result that is found after the search

SUGGESTED_CLICK = driver.find_element_by_class_name("search-results-list__item")
SUGGESTED_CLICK.click()

try:

    # Waiting for daily-weather-list__intervals to be loaded before continuing

    main = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "daily-weather-list__intervals"))
    )
    temperatures = main.find_elements_by_class_name("daily-weather-list-item")

    # Finding the max temperatures and appening them to max_temps and converting them from selenium webElements to text

    for temperature_max in temperatures:
        temperatures_i = temperature_max.find_element_by_class_name("min-max-temperature__max")
        max_temps.append(temperatures_i.text)

    # Finding the min temperatures and appening them to min_temps and converting them from selenium webElements to text

    for temperature_min in temperatures:
        temperature_j = temperature_min.find_element_by_class_name("min-max-temperature__min")
        min_temps.append(temperature_j.text)

    # Finding the dates and appening them to dates and converting them from selenium webElements to text

    for date in temperatures:
        dates_i = date.find_element_by_class_name("date-label")
        dates.append(dates_i.text)

    # Finding the wind speeds and appening them to wind_speed and converting them from selenium webElements to text

    for wind in temperatures:
        wind_i = wind.find_element_by_class_name("wind__container")
        wind_speed.append(wind_i.text)

    for rain in temperatures:
        rain_i = rain.find_element_by_class_name("precipitation__value")
        rain_amount.append(rain_i.text)
except:
    driver.quit()

driver.quit()

# Cleaning up the data so that it's easier to use in the future for other applications

for i, x in enumerate(max_temps):
    max_temps[i] = x.replace("°", '')

for i, x in enumerate(min_temps):
    min_temps[i] = x.replace("°", '')

for i in range(0, len(max_temps)):
    max_temps[i] = int(max_temps[i])

for i in range(0, len(min_temps)):
    min_temps[i] = int(min_temps[i])

for i, x in enumerate(wind_speed):
    wind_speed[i] = x.replace("\n", " ")

for i, x in enumerate(wind_speed):
    wind_speed[i] = x.replace("m/s", "")

# combining max and min.

sum_list = [i + j for (i, j) in zip(max_temps, min_temps)]

# Getting the average temperature.

for i in range(len(sum_list)):
    average.append(sum_list[i]/2)

# Making a pandas dataframe and saving it to data.csv

info = {"Date": dates, "Max temp °C": max_temps, "Min temp °C": min_temps,
        "Average °C": average, "Rain mm": rain_amount, "Wind m/s": wind_speed}
df = pd.DataFrame(info)
print(df)
df.to_csv("data.csv")

