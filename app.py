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

if __name__ == '__main__':
    app.run(debug=True)