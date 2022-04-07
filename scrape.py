from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.common.actions

##
# SELENIUM SETUP
##
driver = webdriver.Chrome('./chromedriver')

##
# STUDENT CALENDAR
##

r = requests.get('https://www.purdue.edu/registrar/calendars/2021-22-Academic-Calendar.html')
data = r.text
soup = BeautifulSoup(data, 'html.parser')
# Main content: div class="maincontent col-lg-9 col-md-9 col-sm-9 right"
# month  <h4>
# <table class "calendarTable"
# day: 'day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
# day of the week: 'weekDay noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
# description: 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'

td = soup.find_all('h4')

months = ['08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06', '07', '08']
dates = []
times = []
descriptions = []
weekdays = []

'''
yearString = soup.find_all(class_="maincontent col-lg-9 col-md-9 col-sm-9 right").find_all("h1")\
    .contents[0].get_text()
yearHyphenYear = re.match('([0-9]*)-([0-9]*)', yearString)
beginYear = yearHyphenYear.group(1)
print("BEGIN YEAR: " + beginYear)
endYear = yearHyphenYear.group(2)
print("END YEAR: " + beginYear)
'''

monthInd = 0
for month in soup.find_all(class_='calendarTable'):
    currMonth = months[monthInd]  # Month the for loop is on
    for event in month.tbody.find_all("tr"):
        for i in range(3):  # Finding day, description, weekday
            content = event.contents[(2*i)+1].get_text()
            if (i == 0):  # Day
                # Extract Day #
                if (len(content) == 1):
                    content = '0' + content
                if (monthInd < 5 and len(content) == 2):
                    dates.append('2021-' + months[monthInd] + '-' + content)
                else: #if(len(content) == 2):
                    dates.append('2022-' + months[monthInd] + '-' + content)

            elif (i == 1):  #Description (time & event)
                # Extract Time #
                time = re.match('(\d*:*\d* [ap].m.)', content)
                if time:
                    times.append(time.group(0))
                else:
                    times.append(None)
                # Extract Event Description #
                desc = re.match('(\d*:*\d* [ap].m.)*([a-zA-Z0-9!@#\\$%\\^\\&*\\)\\(+=\/_\-, ]*)(\n)*', content)
                if desc:
                    descriptions.append(desc.group(2).lstrip())
                else:
                    descriptions.append(None)

            elif (i == 2):  # Weekday
                # Extract Weekday #
                weekday = re.match('([A-Za-z])*(-([A-Za-z]*))*', content)
                if weekday:
                    weekdays.append(weekday.group(0))
                else:
                    weekdays.append(None)
    monthInd += 1

##
# STUDENT DINING
##
courts = {} # Dictionary of dictionaries - each sub dictionary details stations(key) and meals(values)
courtURLs = []
diningMenu = [] # Complete menu

# MENU #

baseDiningURL = 'https://dining.purdue.edu/menus/'

driver.get(baseDiningURL)

# Get list of dining court URLs #

driverCourtURLS = driver.find_elements(By.CLASS_NAME, "menus__home-content--link")
for driverCourtURL in driverCourtURLS:
    courtURLs.append(driverCourtURL.get_attribute('href')) 

#  DINING LIST = [[0-Date, 1-Meal type, 2-Meal Time, 3-Court, 4-Station, 5-Food], [...]]

# Get menu
for courtURL in courtURLs: # Iterate through dining courts
    driver.get(courtURL)
    courtName = driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div/div[1]/a/h1').text
    court = {}

    driver.find_element(By.CLASS_NAME, "datepicker").click() # Activates dropdown menu of dates
    dateElements = driver.find_elements(By.CLASS_NAME, "datepicker-item")
    dateURLS = []
    for dateElement in dateElements:
        dateURLS.append(dateElement.get_attribute('href'))

    mealURLS = []
    for dateURL in dateURLS: # Iterate through available dates
        mealURLS = []
        driver.get(dateURL)
        if courtURLs.index(courtURL) < 7: # If not ON-the-GO location
            driver.find_element(By.CLASS_NAME, "mealpicker").click() # Activates dropdown menu of mealtimes
            mealElements = driver.find_element(By.CLASS_NAME, "mealpicker-menu-meals")
            for mealElement in mealElements.find_elements(By.TAG_NAME, "a"):
                mealURLS.append(mealElement.get_attribute('href'))
        else: # If ON-the-GO location
            mealURLS.append(dateURL) # iffy
            
        for mealURL in mealURLS:
            driver.get(mealURL)
            if driver.find_element(By.CLASS_NAME, "mealpicker-meal-times").text != "Closed": # If dining court is serving that meal
                for station in driver.find_elements(By.CLASS_NAME, "station"): # Iterate through stations in dining court
                    stationName = station.find_element(By.CLASS_NAME, "station-name").text

                    for foodItem in station.find_elements(By.CLASS_NAME, "station-item-text"): # Iterate through food items in station
                        # [0-Date, 1-Meal type, 2-Meal Time, 3-Court, 4-Station, 5-Food]
                        placeholder = True
                        dateItem = driver.find_element(By.CLASS_NAME, "datepicker").text.split("\n")[0] # Format: April 3rd, 2022
                        mealTypeItem = driver.find_element(By.CLASS_NAME, "mealpicker-meal-name").text
                        mealTimeItem = driver.find_element(By.CLASS_NAME, "mealpicker-meal-times").text # Format: 10am - 2pm
                        courtNameItem = driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div/div[1]/a').text # Format: Earhart Dining Court
                        stationNameItem = stationName.partition("\n")[0]
                        foodNameItem = foodItem.text
                        print([dateItem, mealTypeItem, mealTimeItem, courtNameItem, stationNameItem, foodNameItem])
                        diningMenu.append([dateItem, mealTypeItem, mealTimeItem, courtNameItem, stationNameItem, foodNameItem])
                        
for menuItem in diningMenu:
    print(menuItem)

# HOURS #

# Close Webdriver #
driver.close()
