import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



engine  = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def Home():
    return ("Welcome to the API!")

@app.route("/api/v1.0//precipitation")
def precipitation():
        last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
        query_date = dt.date(last_date.year -1, last_date.month, last_date.day)
        sel = [Measurement.date, Measurement.prcp]
        query_result = session.query(*sel).filter(Measurement.date >= query_date).all()
        precipitation_data_list = dict(query_result)
        return jsonify(precipitation_data_list)

@app.route("/api/v1.0/stations")
def stations():
  session  = Session(engine)
  stations_results = session.query(Station.station, Station.name).all()
  return jsonify(stations_results)

if __name__ == "__main__":
    app.run(debug=True)
