from calendar import day_abbr
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import insertData

testing = True # For testing - disables dining scraping

##
# SELENIUM SETUP
##
driver = webdriver.Chrome('BoilermakerBuddy/chromedriver')

##
# CONNECT TO DATABASE
##
mydb, mycursor = insertData.connect()

##
# STUDENT CALENDAR
##

r = requests.get('https://www.purdue.edu/registrar/calendars/2021-22-Academic-Calendar.html')
data = r.text
soup = BeautifulSoup(data, 'html.parser')

td = soup.find_all('h4')

months = ['08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06', '07', '08']
monthsDict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
dates = []
times = []
descriptions = []
weekdays = []

dateRange = False  #If there is a range of dates for an entry
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
                elif(len(content) == 2):
                    dates.append('2022-' + months[monthInd] + '-' + content)
                else:
                    datesMatch = re.match('(\d+)-(\d+)', content)
                    dates.append('2022-' + months[monthInd] + '-' + datesMatch.group(1))
                    dates.append('2022-' + months[monthInd] + '-' + datesMatch.group(2))
                    dateRange = True

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
                    descriptions.append(content.lstrip())
                else:
                    descriptions.append(None)

            elif (i == 2):  # Weekday
                # Extract Weekday #
                weekday = re.match('([A-Za-z])*(-([A-Za-z]*))*', content)
                if weekday:
                    weekdays.append(weekday.group(0))
                else:
                    weekdays.append(None)
                if dateRange:
                    times.append(times[-1])
                    descriptions.append(descriptions[-1])
                    weekdays.append(weekdays[-1])
                    dateRange = False
    monthInd += 1

# Insert Student Calendar data into database #

#Format data
calendarData = [[x] + [y] + [z] + [w] for x, y, z, w in zip(*[iter(dates)], *[iter(weekdays)], *[iter(descriptions)], *[iter(times)])]

#Insert into student_calendar table
insertData.insertStudentCalendar(mydb, mycursor, calendarData)

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
    if testing == True: 
        break
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

                        #Some regex to format dateItem
                        dateTemp = driver.find_element(By.CLASS_NAME, "datepicker").text # Format: April 3rd, 2022
                        dateTemp = re.match('(.*) (\d*), (\d{4})', dateTemp)
                        day = dateTemp.group(2) 
                        if (len(day) == 1):
                            day = '0' + day   
                        dateItem = dateTemp.group(3) + '-' + monthsDict[dateTemp.group(1)] + '-' + dateTemp.group(2) # Format: 2022-04-03                 

                        mealTypeItem = driver.find_element(By.CLASS_NAME, "mealpicker-meal-name").text
                        mealTimeItem = driver.find_element(By.CLASS_NAME, "mealpicker-meal-times").text # Format: 10am - 2pm
                        courtNameItem = driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div/div[1]/a').text # Format: Earhart Dining Court
                        stationNameItem = stationName.partition("\n")[0]
                        foodNameItem = foodItem.text
                        diningMenu.append([dateItem, mealTypeItem, mealTimeItem, courtNameItem, stationNameItem, foodNameItem])

#Format data                        
diningMenu = [tuple(x) for x in diningMenu]

#Insert into dining_courts table
insertData.insertDiningCourts(mydb, mycursor, diningMenu)

# BUILDING ABBREVIATIONS #

buildingInfo = []

driver.get('https://www.purdue.edu/physicalfacilities/units/facilities-operations/building-deputies/directory.html')

buildingTable = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/table/tbody')

for row in buildingTable.find_elements(By.TAG_NAME, "tr"):
    rowElements = row.find_elements(By.TAG_NAME, "td")
    if len(rowElements) != 0: # Ensures something is in row - no errors
        # Split for multiple abbreviations in one entry
        if ',' in rowElements[0].text:
            buildingNames = rowElements[0].text.split(',')
            for name in buildingNames:
                buildingEntry = [name.strip(), rowElements[2].text]
                buildingInfo.append(buildingEntry)
        else: 
            buildingEntry = [rowElements[0].text, rowElements[2].text]
            buildingInfo.append(buildingEntry)

#Format data                        
buildingInfo = [tuple(x) for x in buildingInfo]   

#Insert into dining_courts table
insertData.insertBuildingAbbreviations(mydb, mycursor, buildingInfo)

# Close Webdriver #
driver.close()

# Disconnect from database #
insertData.disconnect(mydb, mycursor)
