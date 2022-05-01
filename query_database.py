from email.utils import formatdate
import mysql.connector
import re
from datetime import datetime

##
# SQL Stuff!
##
DEBUG = 0
##
# Connecting to database
##
def connect():

    try:
        # Connect to database with our login
        mydb = mysql.connector.connect(host="boilermakerbuddydb.c8jck5ubwnj5.us-east-1.rds.amazonaws.com", \
                                       user="admin", password="ECE49595!", database="boilermakerbuddydb")

        mycursor = mydb.cursor()

        return mydb, mycursor

    except mysql.connector.Error as error:
        print("Connection to database failed {}".format(error))


##
# Selecting from student_calendar table
##
def selectStudentCalendar(mycursor):

    try:
        # Select data from tables
        studentCalendarSQL = "SELECT * FROM student_calendar"

        mycursor.execute(studentCalendarSQL)

        studentCalendarData = mycursor.fetchall()

        print(studentCalendarData)

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

#convert (datetime.date(YYYY, MM, DD) to string "Month Day Year"
def dateToString(date):
    d = date.split("-")
    date = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0, 0)
    format = '%A, %B %d, %Y' # Dayofweek, Month day, Year (ex: Monday, January 1st, 2055)

    return date.strftime(format)

##
# Select date given description
##
def selectDateGivenDescription(mycursor, event_description):

    try:
        # Select data from tables
        studentCalendarSQL = "SELECT event_date FROM student_calendar WHERE event_description = '" + event_description + "';"

        mycursor.execute(studentCalendarSQL)

        studentCalendarData = mycursor.fetchall()
        if(DEBUG > 0):
            print(studentCalendarData)
            print(studentCalendarData[0][0])
            print(len(studentCalendarData))
        dateString = ""
        for a in range(len(studentCalendarData)): #if an event has multiple dates
            if(a > 0):
                dateString = dateString + " and "
            dateS = dateToString(str(studentCalendarData[a][0]))
            dateString = dateString + dateS
        return dateString

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

##
# Disconnecting from database
##
def disconnect(mydb, mycursor):
    # Terminate connection upon completion
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySQL connection is closed")

def queryDate(event):

    mydb, mycursor = connect()
    date = selectDateGivenDescription(mycursor, str(event))
    disconnect(mydb, mycursor)
    return date

if __name__ == "__main__":
    mydb, mycursor = connect()
    date = selectDateGivenDescription(mycursor, "CLASSES END")
    print(date)
    disconnect(mydb, mycursor)