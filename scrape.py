from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict

r = requests.get('https://www.purdue.edu/registrar/calendars/2021-22-Academic-Calendar.html')
data = r.text
soup = BeautifulSoup(data, 'html.parser')
# Main content: div class="maincontent col-lg-9 col-md-9 col-sm-9 right"
#month  <h4>

#<table class "calendarTable"
#day: 'day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
#day of the week: 'weekDay noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'
#description: 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'
#[day, time/description, day of week] ?


td = soup.find_all('h4')
times = re.compile('(\d:*\d* [ap].m.)')
#print(soup.find_all(class_ ='day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'))


# for a in soup.find_all(class_ = 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'):
for month in soup.find_all(class_ = 'calendarTable'):
    #for day in month.find_all(class_="day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3"):
        # print(day.get_text())
    for description in month.find_all(class_ = 'description col-lg-11 col-md-10 col-sm-10 col-xs-9'):
        ## TODO MESS WITH THIS LATER ##
        match = times.findall(description.get_text())
        # match = re.split(times, description.get_text(), 1)
        print(match)
    #for weekDay in month.find_all(class_ = 'weekDay noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'):
        # print(weekDay.get_text())
    # print(a.get_text())
#print(td)