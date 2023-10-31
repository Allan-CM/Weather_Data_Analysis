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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database. 
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(latest_date)

    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_date = session.query(Measurement.date, func.round(func.sum(Measurement.prcp), 2)).\
                     filter(Measurement.date >= query_date).\
                     group_by(Measurement.date).\
                     all()

    session.close()

    # Create a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_date}

    # Convert list of tuples into normal list
    precipitation_data = list(np.ravel(precipitation_dict))

    return jsonify(precipitation_data)



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

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #'USC00519281' was determined as the most popular station from our climate started analysis
    latest_date = session.query(Measurement.date).\
              filter(Measurement.station == 'USC00519281').\
              order_by(Measurement.date.desc()).first() 
    print(latest_date)

    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    temp_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= query_date).\
                filter(Measurement.station == 'USC00519281').\
                all()

    session.close()

    # CreatING a dictionary with date as the key and tempearture as the value
    temp_dict = {date: tobs for date, tobs in  temp_data}

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(temp_dict))

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def sd(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #'USC00519281' was determined as the most popular station from our climate started analysis
    date_string = start
    year, month, day = map(int, date_string.split('.'))
    from datetime import datetime
    start_date = datetime(year, month, day)

    # Calculate the date one year from the last date in data set.
    #query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                               filter(Measurement.date >= str(start_date)).\
                               all()
    
    min_temp, avg_temp, max_temp = temp_stats[0]

    temp_dict = {
                "TMIN": min_temp,
                "TAVG": avg_temp,
                "TMAX": max_temp
                }

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    #temp_data = session.query(Measurement.date, Measurement.tobs).\
                #filter(Measurement.date >= query_date).\
                #filter(Measurement.station == 'USC00519281').\
                #all()

    session.close()

    # CreatING a dictionary with date as the key and tempearture as the value
    #temp_dict = {date: tobs for date, tobs in  temp_data}

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(temp_dict))

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def md(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #'USC00519281' was determined as the most popular station from our climate started analysis
    date_string1 = start
    date_string2 = end
    
    year, month, day = map(int, date_string1.split('.'))
    from datetime import datetime
    start_date = datetime(year, month, day)

    year, month, day = map(int, date_string2.split('.'))
    from datetime import datetime
    end_date = datetime(year, month, day)

    # Calculate the date one year from the last date in data set.
    #query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                               filter(Measurement.date <= str(end_date)).\
                               filter(Measurement.date >= str(start_date)).\
                               all()
    
    min_temp, avg_temp, max_temp = temp_stats[0]

    temp_dict = {
                "TMIN": min_temp,
                "TAVG": avg_temp,
                "TMAX": max_temp
                }

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    #temp_data = session.query(Measurement.date, Measurement.tobs).\
                #filter(Measurement.date >= query_date).\
                #filter(Measurement.station == 'USC00519281').\
                #all()

    session.close()

    # CreatING a dictionary with date as the key and tempearture as the value
    #temp_dict = {date: tobs for date, tobs in  temp_data}

    # Convert list of tuples into normal list
    temp_data = list(np.ravel(temp_dict))

    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)