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
# Selecting from student_calendar table
##
def selectStudentCalendar(mycursor):

    try:
        # Select data from tables
        studentCalendarSQL = "SELECT event_date FROM student_calendar WHERE event_description"

        mycursor.execute(studentCalendarSQL)

        studentCalendarData = mycursor.fetchall()

        print(studentCalendarData)

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

if __name__ == "__main__":

    mydb, mycursor = connect()

    selectStudentCalendar(mycursor)

    disconnect(mydb, mycursor)


