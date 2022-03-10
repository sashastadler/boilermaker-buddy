from bs4 import BeautifulSoup
import mysql.connector
import requests
import re
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

##
# SELENIUM SETUP
##
driver = webdriver.Chrome(executable_path='C:\Webdrivers\chromedriver')

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
                elif(len(content) == 2):
                    dates.append('2022-' + months[monthInd] + '-' + content)

            elif (i == 1):  #Description (time & event)
                # Extract Time #
                time = re.match('(\d*:*\d* [ap].m.)', content)
                if time:
                    times.append(time)
                    # print(time.group(1))
                else:
                    times.append(None)  # TODO make sure that this doesn't just append nothing
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
                    weekdays.append(weekday)
                else:
                    weekdays.append(None)
    monthInd += 1

##
# STUDENT DINING
##
courts = {} # Dictionary of dictionaries - each sub dictionary details stations(key) and meals(values)
courtURLs = []

# MENU #
# TODO include for loop of dining courts - testing with Earhart

baseDiningURL = 'https://dining.purdue.edu/menus/'

driver.get(baseDiningURL)

# Get list of dining court URLs #
# CURRENTLY: Scrapes for current data, need to do breakfast, lunch, dinner #
# NEXT: Scrape for whole week #

# Get dining court urls
driverCourtURLs = driver.find_elements(By.CLASS_NAME, "menus__home-content--link")
for driverCourtURL in driverCourtURLs:
    courtURLs.append(driverCourtURL.get_attribute('href')) 

#  DINING LIST =[[0-Date, 1-Meal type, 2-Meal Time, 3-Court, 4-Station, 5-Food], [...]]

# Get menu
for courtURL in courtURLs: # Iterate through dining courts
    driver.get(courtURL)
    courtName = driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div/div[1]/a/h1').text
    court = {}
    # TODO HERE iterate through dates
    # TODO HERE iterate through meal times
    for station in driver.find_elements(By.CLASS_NAME, "station"): # Iterate through stations in dining court
        stationName = station.find_element(By.CLASS_NAME, "station-name").text
        for foodItem in station.find_elements(By.CLASS_NAME, "station-item-text"): # Iterate through food items in station
            if stationName in court: # just fill out DINING LIST at core, use current for loop var names
                court[stationName].append(foodItem.text)
            else:
                court[stationName] = [foodItem.text]
    courts[courtName] = court

# HOURS #

# Close Webdriver #
driver.close()

##
# SQL
##
tempTuple = ()
tempDates = []

for date in dates:
    tempTuple += tuple([date])

data = [x for x in zip(*[iter(dates)])]

mydb = mysql.connector.connect(host="boilermakerbuddydb.c8jck5ubwnj5.us-east-1.rds.amazonaws.com",\
    user="admin", password="ECE49595!", database="boilermakerbuddydb")

# print(mydb)

mycursor = mydb.cursor()

# sql = "INSERT INTO student_calendar (event_date) VALUES %r" %tuple(dates)

datesql = "INSERT INTO student_calendar (event_date) VALUES (%s)"
dowsql = "INSERT INTO student_calendar (event_dow) VALUES ('mon')"
# mycursor.executemany(datesql, data)

mydb.commit()

print(mycursor.rowcount, "record inserted.")