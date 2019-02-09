import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##################################################################################################################################
# Step 2 - Climate App
#
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
#
#
# Use FLASK to create your routes.
#   /
#        Home page
#
#   /api/v1.0/precipitation
#        Convert the query results to a Dictionary using date as the key and prcp as the value.
#        Return the JSON representation of your dictionary.
#    
#   /api/v1.0/stations
#        Return a JSON list of stations from the dataset.
#   
#   /api/v1.0/tobs
#        query for the dates and temperature observations from a year from the last data point.
#        Return a JSON list of Temperature Observations (tobs) for the previous year.
#
#   /api/v1.0/<start> and /api/v1.0/<start>/<end>
#        Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
#            or start-end range.
#        When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#        When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#
#
##################################################################################################################################



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Station = Base.classes.station
Measurement = Base.classes.measurement
# Create our session (link) from Python to the DB
#session = Session(engine)

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
        f"/api/v1.0/precipitation<br/>Returns the JSON list of the precipitation from 8/24/16-8/23/17<br/><br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns a list of Temperature Observations from 8/24/16-8/23/17<br/><br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for August 2016 - August 2017"""
    """Return the JSON representation of your dictionary"""
    # Query for the dates and temperature observations from a year from the last data point
    session = Session(engine)
    
    query_date = dt.date(2017,8, 23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > query_date).\
        order_by(Measurement.date).all()

        
    precip_totals = []
    for result in precip_data:
        measurement_dict = {}
        measurement_dict["date"] = precip_data[0]
        measurement_dict["prcp"] = precip_data[1]
        precip_totals.append(measurement_dict)

    return jsonify(precip_totals)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    # Query all stations
    session = Session(engine)
    results = session.query(Station.station).all()
    
    station_total  = []
    for result in results:
        station_dict = {}
        station_dict["station"] = result[0]
        station_dict["name"] = result[1]
        result.append(station_total)

    return jsonify(station_total) 

  
@app.route("/api/v1.0/tobs")
def tobs():
    #Query for the dates and temperature observations from a year from the last data point
    #Return a JSON list of Temperature Observations (tobs) for the previous year
    session = Session(engine)
  
    query_date = dt.date(2017,8, 23) - dt.timedelta(days=365)
    temp_data = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.date > query_date).\
       order_by(Measurement.date).all()
      
     
    temp_totals = []
    for result in temp_data:
        measurement_dict = {}
        measurement_dict["date"] = temp_data[0]
        measurement_dict["tobs"] = temp_data[1]
        result.append(station_total)

    return jsonify(temp_totals)

	# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
	# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def start_only(date):
	start_dates = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
	return jsonify(start_dates)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start,end):
    date_range_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(date_range_temps)


if __name__ == '__main__':
    app.run(debug=True)
