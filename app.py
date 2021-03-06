import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import timedelta

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
        return (
        f"Welcome To The API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")

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

@app.route("/api/v1.0/tobs")
def tobs():
        one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year).\
                order_by(Measurement.date).all()
        tobs_data_list = list(tobs_data)
        return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        start_day_list = list(start_day)
        return jsonify(start_day_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        start_end_day_list = list(start_end_day)
        return jsonify(start_end_day_list)

if __name__ == "__main__":
    app.run(debug=True)
