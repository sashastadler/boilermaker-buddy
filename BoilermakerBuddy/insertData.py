import mysql.connector

##
# SQL Stuff!
##

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
# Inserting into student_calendar table
##
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

##
# Inserting into dining_courts table
##
def insertDiningCourts(mydb, mycursor, diningMenu):

    try:
        # Clear tables
        clearDiningSQL = "TRUNCATE TABLE dining_courts"
        mycursor.execute(clearDiningSQL)
        print("All records cleared in dining_courts table")

        # Insert data into tables
        diningCourtsSQL = "INSERT INTO dining_courts (meal_date, time_range, meal_type, court_name, station_name, food_name) VALUES (%s, %s, %s, %s, %s, %s)"

        mycursor.executemany(diningCourtsSQL, diningMenu)

        mydb.commit()

        print(mycursor.rowcount, "records inserted in dining_courts table.")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

##
# Inserting into building_abbreviations table
##
def insertBuildingAbbreviations(mydb, mycursor, buildingInfo):

    try:
        # Clear tables
        clearBuildingSQL = "TRUNCATE TABLE building_abbreviations"
        mycursor.execute(clearBuildingSQL)
        print("All records cleared in building_abbreviations table")

        # Insert data into tables
        buildingAbbreviationsSQL = "INSERT INTO building_abbreviations (building_abbreviation, building_name) VALUES (%s, %s)"

        mycursor.executemany(buildingAbbreviationsSQL, buildingInfo)

        mydb.commit()

        print(mycursor.rowcount, "records inserted in building_abbreviations table.")

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

