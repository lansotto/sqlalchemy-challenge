import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from dateutil.relativedelta import relativedelta
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/<start><br/>"
    #    f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Date filter to find last 12 months of data
    dates = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    for d in dates:
        recent = dt.datetime.strptime(d, '%Y-%m-%d').date()
        filter_date = recent - relativedelta(years=1)

    """Return a list of all measurment id"""
    # Query all measurement
    last_12_months = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > filter_date).all()

    session.close()

    all_precipitation = []
    for date, prcp in last_12_months:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/tobs")
def lobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Date filter to find last 12 months of data
    dates = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    for d in dates:
        recent = dt.datetime.strptime(d, '%Y-%m-%d').date()
        filter_date = recent - relativedelta(years=1)

    """Return a list of all measurment id"""
    # Query all measurement
    tobs_result = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first()
    most_active_station = tobs_result[0]
    
    most_active_station_12_months = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > filter_date).\
    filter(Measurement.station == most_active_station).all()

    session.close()

    all_temperature = []
    for date, tobs in most_active_station_12_months:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["temperature"] = tobs
        all_temperature.append(temperature_dict)
    
    return jsonify(all_temperature)

@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data of each station"""
    # Query all stations
    station_results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for id, station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/<start>")
def start(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Create a dictionary with minimum, maximum and average temperatures
       
    specified_start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    sel = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= specified_start).all()
    after_specified_start_final = list(np.ravel(sel))
    session.close()

    return jsonify(after_specified_start_final)

#@app.route("/api/v1.0/<start>/<end>")
#def start(start=None):
    # Create our session (link) from Python to the DB
#    session = Session(engine)
    
    # Create a dictionary with minimum, maximum and average temperatures
       
#    specified_start = dt.datetime.strptime(start, '%Y-%m-%d').date()
#    sel = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
#        filter(Measurement.date >= specified_start).all()
#    after_specified_start_final = list(np.ravel(sel))
#    session.close()

#    return jsonify(after_specified_start_final)

if __name__ == '__main__':
    app.run(debug=True)
