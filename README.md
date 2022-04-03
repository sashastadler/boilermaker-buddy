# Users
### Installation
To install the skill, go to the Alexa Skills store in the Alexa app or from the Alexa website. Then search for our skill under the name "Boilermaker Student Buddy" and install. No further setup is required and the skill is ready to be used from any Alexa-enabled device.

### Use
Launch the skill with the phrase "Open Boilermaker Buddy" or anything similar. Once launched, users can request information, following the example requests provided in the skill information section, by asking "what can I ask?", "What can boilermaker buddy do?", to prompt the skill to recommend questions to ask. 

#### Supported topics:

- Academic calendar information
- Purdue Dining menus*
- Building information*
- Club information*

\*In development

# Developers

The structure of the Boilermaker Buddy can be separated into three parts: The python code, the AWS Lambda server, and the AWS mySQL relational database.

### Repository Structure

The repository has two branches: one for the information gathering and uploading to the SQL database, another for the Alexa Skill handling (information retrieval and delivery). The Alexa Skill handler branch includes the JSON file of the skill configuration information (including slot and intent info). The branches get merged into the main branch when they are stable. 

## Python

The python code is structured into three separate areas: Student calendar web scraping, dining court menu web scraping, and building information web scraping.  At the end of the python code, the scraped information is uploaded to the SQL database for the AWS Lambda server to reference.

### Student Calendar

The student calendar information is scraped using the BeautifulSoup python library.

The code uses a for loop to cycle through the months found in the HTML of the webpage for the student calendar (https://www.purdue.edu/registrar/calendars/2021-22-Academic-Calendar.html).  For each month, the code cycles through the events listed for that month.  Each event has three attributes that are collected: The date of the event, the description of the event (event time and event name), and the weekday that the event takes place on.   

Each of these attributes are placed into their own list and are uploaded to the SQL database at the end of the code.

### Dining Court Menus

The dining court information is scraped using Selenium with the Chromium webdriver in order to navigate between web pages with ease.

We use Selenium to first take the home page of the Purdue dining court menu (https://dining.purdue.edu/menus/) and find the URL for each dining court.  From this list of dining court URLs, we navigate to each of them using the get() command for our webdriver.

For each dining court, we cycle through a.) the dates available in advance (ex. today’s meals, tomorrow’s meals, etc.) and b.) the meal times (ex. breakfast, lunch, dinner).  For each of the meal times on a date, we cycle through the various meal stations that are at the dining court and collect what food is there.  

This data is stored in a list of lists called dining_list, where each element is a list in the format of: [“date”, “time range meal is available”, “breakfast/lunch/dinner”, “dining court name”, “station name”, “food name”].  This sublist is filled out at the innermost level of the for-loop collecting this data and is appended to dining_list.

The elements of dining_list are then uploaded into our SQL database at the end of the code.

### Building Information

Building information web scraping is currently in progress.  No information is available about this section.

## AWS Lambda

The lambda function is what the Alexa Skill uses to handle user requests using the Alexa Skill SDK. There is one handler for each table of information that is in the SQL database. Additionally, each handler is documented in the JSON configuration file, which also lists the possible utterances that are meant to trigger that handler and the slots (and acceptable slot values and synonyms) for each handler.

## SQL

A MySQL relational database named boilermakerBuddyDB is used with three tables, with one table storing student calendar information, another storing dining court information, and the last storing building hour information.

### Student Calendar Table
- Name: student_calendar
- Attributes 
  - Event Date
    - Description: Date of event entry
    - Name: event_date
    - Data type: date
    - Key: None
    - Constraints: None
  - Event Time 
    - Description: Time of event entry
    - Name: event_time
    - Data type: time
    - Key: None
    - Constraints: None 
  - Event Description
    - Description: Description of event entry
    - Name: event_description
    - Data type: varchar(150)
    - Key: None
    - Constraints: None
  - Event Day of Week
    - Description: Day of week of event (Monday, Tuesday, …)
    - Name: event_dow
    - Data type: varchar(3)
    - Key: None
    - Constraints: None
    
### Dining Court Table
- Name: dining_courts
- Attributes 
  - Meal Date
    - Description: Date of meal entry
    - Name: meal_date
    - Data type: date
    - Key: None
    - Constraints: NOT NULL
  - Time Range
    - Description: Time range meal is available
    - Name: time_range
    - Data type: varchar(20)
    - Key: None
    - Constraints: NOT NULL
  - Meal Type
    - Description: Type of meal (lunch/breakfast/dinner)
    - Name: meal_type
    - Data type: varchar(10)
    - Key: None
    - Constraints: NOT NULL
  - Court Name
    - Description: Name of dining court (Ford, Wiley, etc.)
    - Name: court_name
    - Data type: varchar(20)
    - Key: None
    - Constraints: NOT NULL
  - Station Name
    - Description: Name of food station (BoilerQ, Sugar Hill, etc.)
    - Name: station_name
    - Data type: varchar(20)
    - Key: None
    - Constraints: NOT NULL
  - Food Name
    - Description: Name of food (Hamburgers, Thin Cut Fries, etc.)
    - Name: food_name
    - Data type: varchar(20)
    - Key: None
    - Constraints: NOT NULL

### Building Hour Information
In progress…

