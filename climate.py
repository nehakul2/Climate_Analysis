from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from flask import Flask, jsonify
from datetime import datetime,timedelta


import climate_analysis as helper


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/temperature<br>\
            /api/v1.0/stations<br>\
            /api/v1.0/start<br>\
            /api/v1.0/startend")
            
            
#Query for the dates and temperature observations from the last year.

@app.route("/api/v1.0/precipitation")
def getprecipitationinfo():
   sdate = datetime.now()
   #print("!!!!!!!!!!!!",sdate)
   startdate=datetime.date(sdate)
   precipitation_df = helper.flask_precipitation_data(startdate)
   precipitation_list = precipitation_df.to_dict(orient='index')
   result = jsonify(precipitation_list)
   return result
	
@app.route("/api/v1.0/stations")
def getstationinfo():
   station_df = helper.station_data()
   station_list = station_df.to_dict(orient='index')
   result1 = jsonify(station_list)
   return result1

@app.route("/api/v1.0/tobs")
def gettempinfo():
   sdate = datetime.now()
   #print("!!!!!!!!!!!!",sdate)
   startdate=datetime.date(sdate)
   temp_df = helper.flask_temp_data(startdate)
   temp_list = temp_df.to_dict(orient='index')
   result4 = jsonify(temp_list)
   return result4 
   
@app.route("/api/v1.0/start")
def getstartdateinfo():
   startdate = '2016-01-01'
   station_df = helper.flask_start_temps(startdate)
   station_list = station_df.to_dict(orient='index')
   result2 = jsonify(station_list)
   return result2
   
@app.route("/api/v1.0/startend")
def getstartenddateinfo():
   sdate = datetime.now()
   startdate=datetime.date(sdate)
   enddate = startdate - timedelta(days=365)
   startdate = '2016-01-01'
   enddate = '2017-01-01'
   station_df = helper.flask_calc_temps(startdate,enddate)
   station_list = station_df.to_dict(orient='index')
   result3 = jsonify(station_list)
   return result3     
	
app.run(port=5000)