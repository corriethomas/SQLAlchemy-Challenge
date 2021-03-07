import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    """List all available routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data including the date"""
    #Rubric and Readme do not match, one asks for precipitation data and one asks for last year of data
    session = Session(engine)

    precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all() 

    session.close()

    all_precip = []
    for list_year, list_precip in precip_results:
        prcp_dict = {}
        prcp_dict["date"] = list_year
        prcp_dict["prcp"] = list_precip
        all_precip.append(prcp_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    #Rubric and Readme do not match, one asks for list of stations and one asks for all station info
    session = Session(engine)

    station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = []
    for station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temps and dates of most active station for last year of data"""
    session = Session(engine)

    temp_results = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date >= "2016-08-18") & (Measurement.station == "USC00519281")).all()

    session.close()

    station_temps = []
    for temp_date, tobs in temp_results:
        temp_dict = {}
        temp_dict["date"] = temp_date
        temp_dict["tobs"] = tobs
        station_temps.append(temp_dict)

        return jsonify(station_temps)

if __name__ == '__main__':
    app.run(debug=True)