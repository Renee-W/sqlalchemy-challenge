import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={"check_same_thread":False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement=Base.classes.measurement
Station=Base.classes.station
session=Session(engine)

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
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/(start)<br/>"
        f"/api/v1.0/temp/(start)/(end)<br/>"
    )

@app.route("/api/v1.0/precipitation")
#Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
def precipitation():
    pre_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    pre_year_data=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=pre_year).all()
    results={date:precp for date,precp in pre_year_data}
    return jsonify(results=results)

@app.route("/api/v1.0/stations")
#stations
def stations():
    results=session.query(Station.station).all()
    stations=list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
# Query the dates and temperature observations of the most active station for the last year of data.
def tobs():
    pre_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    pre_year_data=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=pre_year).all()
    results={date:tobs for date,tobs in pre_year_data}
    return jsonify(results=results)

@app.route("/api/v1.0/temp/<start>")
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    if not end:
        results=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
        unravel=list(np.ravel(results))
        return jsonify(results=results)
    
    results=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    unravel=list(np.ravel(results))
    return jsonify(results=results)
    

if __name__ == '__main__':
    app.run()
