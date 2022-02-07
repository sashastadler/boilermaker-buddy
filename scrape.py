from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict
import mysql.connector

r = requests.get('https://www.purdue.edu/registrar/calendars/2021-22-Academic-Calendar.html')
data = r.text
soup = BeautifulSoup(data, 'html.parser')
# Main content: div class="maincontent col-lg-9 col-md-9 col-sm-9 right"
#month  <h4>

#<table class "calendarTable"
#day: 'day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
#day of the week: 'weekDay noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
#description: 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'

## REGEX SECTION ##
td = soup.find_all('h4')
# time = re.compile('(\d:*\d* [ap].m.)')
# time_event = '(\d:*\d* [ap].m.)((\w|\W)*)'

# {event : [month, dow, day, time], event2 : ...}
testlist = [] # for testing
dates = []
months = ['08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06', '07', '08']
'''
yearString = soup.find_all(class_ = "maincontent col-lg-9 col-md-9 col-sm-9 right").find_all("h1").contents[0].get_text()
yearHyphenYear = re.match('(\d*)-(\d*)', yearString)
beginYear = yearHyphenYear.group(1)
print("BEGIN YEAR: " + beginYear)
endYear = yearHyphenYear.group(2)
print("END YEAR: " + beginYear)
'''


# for a in soup.find_all(class_ = 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'):
monthInd = 0
for month in soup.find_all(class_ = 'calendarTable'):
    currMonth = months[monthInd] # Month the for loop is on
    for event in month.tbody.find_all("tr"):
        for i in range(3): # Finding day, description, weekday
            content = event.contents[(2*i)+1].get_text()

            if (i == 0): # Day
                # TODO fix hyphen dates/check to make sure all dates are there
                if(len(content) == 1):
                    content = '0' + content                
                if(monthInd < 5 and len(content) == 2):
                    dates.append('2021-' + months[monthInd] + '-' + content) # TODO look into scraping year from website - might be in header?
                elif(len(content) == 2):
                    dates.append('2022-' + months[monthInd] + '-' + content)

            elif (i == 1): #Description (time & event)
                # Extract Time #
                time = re.match('(\d*:*\d* [ap].m.)', content)
                if time:
                    placeholder_variable = 0
                    # print(time.group(1))
                else:
                    time = None
                    # no time? what do store time as 0? or other placeholder that we understand to mean All-Day event
                # Extract Event Description #
                '''
                desc = re.match('([a-zA-Z0-9!@#\\$%\\^\\&*\\)\\(+=\/_\-, ]*$)', content)
                if desc:
                    print(desc.group(1))
                '''
            elif (i == 2): # Weekday
                testlist.append(content) # CHANGE - don't keep testlist

    monthInd += 1
                    
#print(dates)
tempTuple = ()
tempDates = []

for date in dates:
    tempTuple += tuple([date])

data = [x for x in zip(*[iter(dates)])]
# print(data)

mydb = mysql.connector.connect(host="boilermakerbuddydb.c8jck5ubwnj5.us-east-1.rds.amazonaws.com", user="admin", password="ECE49595!", database="boilermakerbuddydb")

# print(mydb)

mycursor = mydb.cursor()


# sql = "INSERT INTO student_calendar (event_date) VALUES %r" %tuple(dates)

datesql = "INSERT INTO student_calendar (event_date) VALUES (%s)"
dowsql = "INSERT INTO student_calendar (event_dow) VALUES ('mon')" 
mycursor.executemany(datesql, data)

mydb.commit()

print(mycursor.rowcount, "record inserted.")



#print(testlist)
           
      
    # print(month.tbody.tr.contents[7].get_text())
    # get day
    # get description
    # get weekday
'''
for description in month.find_all(class_ = 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'):
    # Get event name
    ## TODO MESS WITH THIS LATER ##
    time_text = description.find("strong").get_text()
    match = time.findall(time_text)
    # match = time.findall(description.get_text()) # times
    # match = re.split(times, description.get_text(), 1)
    print(match)
for day in month.find_all(class_="day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3"):
    print(day.get_text())

#for weekDay in month.find_all(class_ = 'weekDay noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'):
    # print(weekDay.get_text())
# print(a.get_text())
'''
#print(td)


# [Event] [Month] [DoW] [Day] [Time]  