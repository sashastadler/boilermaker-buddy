from bs4 import BeautifulSoup
import mysql.connector
import requests
import re

r = requests.get('https://www.purdue.edu/registrar/calendars/2021-22-Academic-Calendar.html')
data = r.text
soup = BeautifulSoup(data, 'html.parser')
# Main content: div class="maincontent col-lg-9 col-md-9 col-sm-9 right"
# month  <h4>

# <table class "calendarTable"
# day: 'day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
# day of the week: 'weekDay noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
# description: 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'

# REGEX SECTION #
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
                # TODO fix hyphen dates/check to make sure all dates are there
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
                weekday = re.match('([A-Za-z])*(-([A-Za-z]*))*', content)
                if weekday:
                    weekdays.append(weekday)
                    print(weekday)
                else:
                    weekdays.append(None)

    monthInd += 1

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
