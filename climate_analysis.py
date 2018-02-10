
# coding: utf-8

# ### Climate Analysis and Exploration

# Import our dependencies
import pandas as pd
import os
from pathlib import Path
import csv
import matplotlib.pyplot as plt
import numpy as np


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.sql import label
from sqlalchemy import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import Column, Integer, String, Numeric, Text, Float,Table,ForeignKey
from flask import jsonify

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib

from datetime import datetime,timedelta


# Use a Session to test the Measurement class
engine = create_engine("sqlite:///hawaii.sqlite")


# Declare a Base using `automap_base()`
Base = automap_base()

Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station


# create a session
session = Session(engine)
my_table = Table('Measurement', Base.metadata,
   Column("station", String, ForeignKey("Station.station")),
   autoload=True,autoload_with=engine)


#checking data in the measurement table
engine.execute('SELECT * FROM measurement LIMIT 10').fetchall()


#checking data in the station table
engine.execute('SELECT * FROM station LIMIT 10').fetchall()



# Start a session to query the database
session = Session(engine)


engine.execute("select * from measurement limit 5").fetchall()


start_date = '2010-01-01'


end_date = '2011-01-01'



# Query measurements table and save the query into results
results = engine.execute("select * from measurement limit 5").fetchall()
current_time = datetime.now()
past_year = current_time - timedelta(days=365)
measurements_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > past_year).all()


# ### Precipitation Analysis



def precipitation_data():
   #Get date for last year
   current_time = datetime.now()
   past_year = current_time - timedelta(days=365)
   measurements_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > past_year).all()
   
   #created dictionary to get the data
   measure_records = []
   for measure in measurements_year:
       measure_records.append(measure._asdict())
   
   #dictionary to dataframe
   measurements_df = pd.DataFrame.from_records(measure_records)
   measurements_df = measurements_df.set_index('date')

   return measurements_df




prec_df=precipitation_data()
prec_df.head()




prec_df.plot(kind="line" , linewidth = 4,  color='b',alpha=0.5,figsize=(15,10),rot=340)
plt.title("Precipitation Analysis")
plt.xlabel("Date")
plt.ylabel("Precipitation")
plt.tight_layout()

plt.show()


# ### Station Analysis



#Design a query to calculate the total number of stations.
engine.execute("select * from station").fetchall()




#Creating the query to get active stations
active_stations = session.query(Station.name,Station.station,label('number_of_obs',func.count(Measurement.id))).                   filter(Measurement.station == Station.station).group_by(Station.name,Station.station).order_by(func.count(Measurement.id).desc())




#Design a query to find the most active stations.
#List the stations and observation counts in descending order

def station_data():
   active_stations = session.query(Station.name,Station.station,label('number_of_obs',func.count(Measurement.id))).                   filter(Measurement.station == Station.station).group_by(Station.name,Station.station).order_by(func.count(Measurement.id).desc())
   #created dictionary to get the data
   measure_records = []
   for measure in active_stations:
       measure_records.append(measure._asdict())
   
   #dictionary to dataframe
   measurements_df = pd.DataFrame.from_records(measure_records)

   return measurements_df



station_df=station_data()
station_df.head()



#Which station has the highest number of observations?
station_id = station_df.iloc[:1]['station'][0]
print("Station with highest number of observations  is : " ,station_id)




def temp_data():
   #Get date for last year
   current_time = datetime.now()
   past_year = current_time - timedelta(days=365)
   measurements_year = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > past_year).filter(Measurement.station ==station_id).all()
   
   #created dictionary to get the data
   measure_records = []
   for measure in measurements_year:
       measure_records.append(measure._asdict())
   
   #dictionary to dataframe
   measurements_df = pd.DataFrame.from_records(measure_records)
   measurements_df = measurements_df.set_index('date')

   return measurements_df




tobs_df= temp_data()
tobs_df.head()




#draw histogram for temperature
tobs_df.plot.hist(alpha=0.5,bins=12 ,figsize=(10,10))

plt.xlabel('Tobs')
plt.ylabel('Freuency')
plt.title('Histogram of : temperature observation data')
plt.show()


# ### Temperature Analysis




#Write a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d` and return the minimum, average, and maximum temperatures for that range of dates.
#startdate = "2016-01-02"
#enddate = "2017-01-02"

def calc_temps(startdate,enddate):
  temperature_vacation = session.query(label('max_temp',func.max(Measurement.tobs)),                                   label('min_temp',func.min(Measurement.tobs)),                                   label('avg_temp',func.avg(Measurement.tobs))).                  filter(Measurement.date >= startdate).                  filter(Measurement.date <= enddate )

  Max_temp = temperature_vacation[0].max_temp
  Min_temp = temperature_vacation[0].min_temp
  Avg_temp = temperature_vacation[0].avg_temp

  print("Tempture for date range:",Max_temp ,Min_temp,Avg_temp)
  print("Last year tempature for same date range :Max Temp,MIN temp,Avg temp :", Max_temp,Min_temp,Avg_temp)
  
  yerror = Max_temp - Min_temp
  
  barvalue = [Avg_temp]
  xvals = range(len(barvalue))
  matplotlib.rcParams.update({'font.size': 12})
  
  fig,ax = plt.subplots(figsize=(5,8))
  ax.bar(xvals, barvalue, yerr=yerror, color='g',alpha=0.6)
  ax.set_xticks([1])
  plt.xlabel("Vacation time period")
  plt.ylabel("Temperature")
  plt.title("Trip average temperature")
  plt.tight_layout()
  plt.savefig("Tripavg.png")
  
  plt.show() 

#asking the user to enter the startdate and calculating the end date
import datetime

sdate = input("please enter the start date in the format `%Y-%m-%d` :")
startdate=datetime.datetime.strptime(sdate, "%Y-%m-%d")
enddate = startdate + datetime.timedelta(days=365)
calc_temps(startdate,enddate)




from flask import Flask
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available Routes:<br/> \ /api/v1.0/precipitation<br/> \ /api/v1.0/stations <br/> \/api/v1.0/start <br/>             /api/v1.0/start/end <br/>" 
            )


#Query for the dates and temperature observations from the last year.
@app.route("/api/v1.0/precipitation")
def precipitation():
   #Get date for last year
   current_time = datetime.now()
   past_year = current_time - timedelta(days=365)
   measurements_year = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > current_time).filter(Measurement.date  < past_year).all()
   
   #created dictionary to get the data
   measure_records = []
   for measure in measurements_year:
       measure_records.append(measure._asdict())
   
   #dictionary to dataframe
   measurements_df = pd.DataFrame.from_records(measure_records)
   measurements_df = measurements_df.set_index('date')

   return jsonify(measurements_df)



# Return a json list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""
    # Query all passengers
    results = session.query(station).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        all_stations.append(station_dict)

    return jsonify(all_stations)


#Return a json list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs_data():
   #Get date for last year
   current_time = datetime.now()
   past_year = current_time - timedelta(days=365)
   measurements_year = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > current_time).filter(Measurement.date  < past_year).all()
   
   #created dictionary to get the data
   measure_records = []
   for measure in measurements_year:
       measure_records.append(measure._asdict())
   
   #dictionary to dataframe
   measurements_df = pd.DataFrame.from_records(measure_records)
   measurements_df = measurements_df.set_index('date')

   return jsonify(measurements_df) 

#Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/start")
def start_temps(startdate):
  temperature_vacation = session.query(label('max_temp',func.max(Measurement.tobs)), 
                                       label('min_temp',func.min(Measurement.tobs)),
                                       label('avg_temp',func.avg(Measurement.tobs))).filter(Measurement.date >= startdate).filter(Measurement.date <= enddate )

  Max_temp = temperature_vacation[0].max_temp
  Min_temp = temperature_vacation[0].min_temp
  Avg_temp = temperature_vacation[0].avg_temp

  print("Tempture for date range in start api is:",Max_temp ,Min_temp,Avg_temp)
  print("Last year tempature for same date range :Max Temp,MIN temp,Avg temp :", Max_temp,Min_temp,Avg_temp)
  
  #yerror = Max_temp - Min_temp
  return jsonify(Min_temp,Max_temp,Avg_temp)
  
  
@app.route("/api/v1.0/start/end")
def start_end_temps(startdate,enddate):
  temperature_vacation = session.query(label('max_temp',func.max(Measurement.tobs)),
                                       label('min_temp',func.min(Measurement.tobs)), 
                                       label('avg_temp',func.avg(Measurement.tobs))).filter(Measurement.date >= startdate).filter(Measurement.date <= enddate )

  Max_temp = temperature_vacation[0].max_temp
  Min_temp = temperature_vacation[0].min_temp
  Avg_temp = temperature_vacation[0].avg_temp

  print("Tempture for date range in start -end api is :",Max_temp ,Min_temp,Avg_temp)
  print("Last year tempature for same date range :Max Temp,MIN temp,Avg temp :", Max_temp,Min_temp,Avg_temp)
  return jsonify(Min_temp,Max_temp,Avg_temp)
  
#start_end_temps(startdate,enddate)
