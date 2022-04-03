import mysql.connector

##
# SQL Stuff!
##

# Format data to insert into MySQL tables
#calendarData = [[x] + [y] + [z] + [w] for x, y, z, w in zip(*[iter(dates)], *[iter(weekdays)], *[iter(descriptions)], *[iter(times)])]

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

def insertStudentCalendar(mydb, mycursor, calendarData):

    try:
        # Clear tables
        clearDatesSQL = "TRUNCATE TABLE student_calendar"
        mycursor.execute(clearDatesSQL)
        print("All records cleared in student_calendar table")

        # Insert data into tables
        studentCalendarSQL = "INSERT INTO student_calendar (event_date, event_dow, event_description, event_time) VALUES (%s, %s, %s, %s)"

        mycursor.executemany(studentCalendarSQL, calendarData)

        mydb.commit()

        print(mycursor.rowcount, "records inserted in student_calendar table.")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

def disconnect(mydb, mycursor):
    # Terminate connection upon completion
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySQL connection is closed")

