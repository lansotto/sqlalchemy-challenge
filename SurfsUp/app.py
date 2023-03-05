import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    dates = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    for d in dates:
    
    from dateutil.relativedelta import relativedelta
    recent = dt.datetime.strptime(d, '%Y-%m-%d').date()
    filter_date = recent - relativedelta(years=1)
    filter_date

    """Return a list of all measurment id"""
    # Query all measurement
    last_12_months = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > filter_date).all()

    session.close()

    # Convert list of tuples into normal list
    last_12_months_normal = list(np.ravel(last_12_months))

    return jsonify(last_12_months_normal)

@app.route("/api/v1.0/tobs")
def lobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurment id"""
    # Query all measurement
    results = session.query(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))

    return jsonify(all_dates)

@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data of each station"""
    # Query all stations
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
