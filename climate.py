from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData

from flask import Flask, jsonify

import climate_analysis.py
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
print("Connected to DB")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print("Reflected tables")


# Use MetaData from SQLAlchemy to reflect the tables
metadata = MetaData(bind=engine)
metadata.reflect()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#checking data in the measurement table
table = sqlalchemy.Table('measurement', metadata, autoload=True)

# Test that the insert works by fetching the first 5 rows. 
conn.execute("select * from measurement limit 5").fetchall()



app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available Routes:<br/> \ /api/v1.0/precipitation<br/> \ /api/v1.0/stations <br/> \/api/v1.0/start <br/>             /api/v1.0/start/end <br/>" 
            )


#Query for the dates and temperature observations from the last year.

@app.route("/api/v1.0/precipitation")
def getprecipitationinfo():
   precipitation_df = precipitation_data()
   precipitation_list = precipitation_df.to_dict(orient='index')
   result = jsonify(precipitation_list)
   return result

app.run(port=5000)