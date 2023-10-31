# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"**For date fir the next few api using YYYY.MM.DD<br/>"
        f"/api/v1.0/(replace w/ start date)<br/>"
        f"/api/v1.0/(replace w/ start date)/(replace w/ end date)"
    )

#Creating route to preceiptation API
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database. 
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(latest_date)

    # Calculate the date one year from the last date in data set as determined by the code above and hardcoded
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_date = session.query(Measurement.date, Measurement.prcp).\
                     filter(Measurement.date >= query_date).\
                     all()

    #Closing Session
    session.close()

    # Create a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_date}

    # Convert list of tuples into normal list
    precipitation_data = list(np.ravel(precipitation_dict))

    #Jsonifying out data
    return jsonify(precipitation_data)


#Creating route to Station API
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Design a query to return a list of station
    station_list = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_data = list(np.ravel(station_list))

    return jsonify(station_data)

#Creating route to Temperature Observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Querying the most popular station
    active_stations = session.query(Measurement.station, Station.name, func.count(Station.station)).\
                  filter(Measurement.station == Station.station).\
                  group_by(Station.station).\
                  order_by(func.count(Station.station).desc()).\
                  first()

    #Unpacking data from the above query 
    station_id, station_name, station_count = active_stations 

    #Querying data for latest date for the most popular station
    latest_date = session.query(Measurement.date).\
              filter(Measurement.station == station_id).\
              order_by(Measurement.date.desc()).first() 
    print(latest_date)

    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    temp_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= query_date).\
                filter(Measurement.station == station_id).\
                all()

    session.close()

    # CreatING a dictionary with date as the key and tempearture as the value
    temp_dict = {date: tobs for date, tobs in temp_data}

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(temp_dict))

    return jsonify(temp_data)

#Creating route to retrieve temperature data for the start date inputted by user
@app.route("/api/v1.0/<start>")
def sd(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Taking user inputted date and converting it to a datetime variable
    date_string = start
    year, month, day = map(int, date_string.split('.'))
    from datetime import datetime
    start_date = datetime(year, month, day)
    

    #Querying min, max, and average temperature filtering data using the provided start date 
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                               filter(Measurement.date >= str(start_date)).\
                               all()
    
    #Unpacks the query into seperate vairable
    min_temp, avg_temp, max_temp = temp_stats[0]

    #loads variable date intoa dictonary
    temp_dict = {
                "TMIN": min_temp,
                "TAVG": avg_temp,
                "TMAX": max_temp
                }

    #close session 
    session.close()

    # Convert dictonary into normal list
    temp_data = list(np.ravel(temp_dict))

    return jsonify(temp_data)

#Creating route to retrieve temperature data for the specifed start date and end date inputted by user
@app.route("/api/v1.0/<start>/<end>")
def md(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Storing user inputted date into a variable
    date_string1 = start
    date_string2 = end
    
    #Taking user inputted start date and converting it to a datetime variable
    year, month, day = map(int, date_string1.split('.'))
    from datetime import datetime
    start_date = datetime(year, month, day)

    #Taking user inputted end date and converting it to a datetime variable
    year, month, day = map(int, date_string2.split('.'))
    from datetime import datetime
    end_date = datetime(year, month, day)

    #Querying min, max, and average temperature filtering data using the provided start date 
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                               filter(Measurement.date <= str(end_date)).\
                               filter(Measurement.date >= str(start_date)).\
                               all()
    
    #Unpacks the query into seperate vairable
    min_temp, avg_temp, max_temp = temp_stats[0]

    #loads variable date intoa dictonary
    temp_dict = {
                "TMIN": min_temp,
                "TAVG": avg_temp,
                "TMAX": max_temp
                }

    session.close()

    #Converts dictonary into normal list
    temp_data = list(np.ravel(temp_dict))

    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)