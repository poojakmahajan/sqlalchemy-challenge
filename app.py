
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for Home page")
    return(
        f"Welcome to the Home page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    retrieve_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year_date).all()
    retrieve_data_dict = dict(retrieve_data)
    session.close()
    return jsonify(retrieve_data_dict)

#Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    st = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    st_dict = dict(st)
    session.close()
    return jsonify(st_dict)

#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def temperature():
    last_12months_temp = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date >= 2016,8,23).filter(Measurement.station == 'USC00519281').all()
    last_12months_temp_dict = dict(last_12months_temp)
    session.close()
    return jsonify(last_12months_temp_dict)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.



if __name__ == "__main__":
    app.run(debug=True)