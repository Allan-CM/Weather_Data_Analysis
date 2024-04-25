# Weather Data Analysis and API Development README

## Overview
This project involves the analysis of weather data stored in an SQLite database using SQLAlchemy ORM and the development of a Flask API to expose this data through various endpoints. The analysis includes exploratory precipitation analysis and station analysis, followed by the creation of API routes to retrieve precipitation data, station information, and temperature observations based on user input.

## Project Structure

### Dependencies and Libraries
* Matplotlib: For data visualization
* Numpy: For numerical operations
* Pandas: For data manipulation and analysis
* Datetime: For date and time operations
* SQLAlchemy: For SQL database interaction
* Flask: For API development

### Database Setup
* Database: hawaii.sqlite
* Tables: Measurement and Station

## Exploratory Analysis
### Precipitation Analysis
* Latest Date: Retrieve the most recent date from the dataset
* Date Range: Calculate the date range for the last 12 months of data
* Data Retrieval: Query precipitation data within the date range
* Data Visualization: Plot precipitation data as a bar graph
### Station Analysis
* Total Stations: Calculate the total number of stations
* Most Active Stations: Identify the most active station based on observation counts
* Temperature Statistics: Calculate lowest, highest, and average temperatures for the most active station
* Temperature Observations: Query temperature data for the last 12 months and plot as a histogram

# Flask API Development
## API Endpoints
1. Root
* '/' - Lists available API routes
2. Precipitation
* '/api/v1.0/precipitation' - Retrieves precipitation data for the last 12 months
3. Stations
* '/api/v1.0/stations'- Retrieves a list of stations
  . Temperature Observations
* '/api/v1.0/tobs' - Retrieves temperature observations for the last 12 months from the most active station
4. Temperature Statistics by Start Date
* '/api/v1.0/<start>' - Retrieves min, avg, and max temperatures from the start date to the latest date
5. Temperature Statistics by Start and End Date
* '/api/v1.0/<start>/<end>'- Retrieves min, avg, and max temperatures between the specified start and end dates

# Conclusion
This project provides a comprehensive approach to weather data analysis and API development. The exploratory analysis offers insights into precipitation patterns and station activities, while the Flask API offers a user-friendly interface to access this information. Whether you're interested in historical weather data or current station details, this project serves as a valuable resource for retrieving and analyzing weather-related information.

# Resources Folder: 
1. hawaii.sqlite --> SQlite file used for data analysis
2. hawaii_measurements --> hawaii measurement data csv
3. hawaii_station --> hawaii station data csv 

# SurfsUp Folder: 
1. app.py--> Contains the python code to create API for various database queries
2. climate_starter --> Jupyter notebook that contains the code for the analysis of the variaous databse queries that were conducted. 

# Credits: 
https://matplotlib.org/stable/api/dates_api.html --> taught me how to manipulate the x tick location of my grpah using the datelocator module from matplotlib

