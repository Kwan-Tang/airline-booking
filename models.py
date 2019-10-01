import csv
import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
engine = db.create_engine(config.uri,{})
meta = db.MetaData(bind=engine,reflect=True)

class Flight(db.Model):
    __tablename__="flights"
    id = db.Column(db.Integer,primary_key=True)
    origin_id = db.Column(db.Integer,db.ForeignKey("airports.id"),nullable=False)
    destination_id = db.Column(db.Integer,db.ForeignKey("airports.id"),nullable=False)
    duration = db.Column(db.String,nullable=False)
    passengers = db.relationship("Passenger",backref="flight",lazy=True)

    def add_passenger(self,name):
        p = Passenger(name=name,flight_id=self.id)
        db.session.add(p)
        db.session.commit()

    def preload_flights():
        f = open("flights_data.csv")
        reader = csv.reader(f)
        for origin_id,destination_id,duration in reader:
            flight = Flight(origin_id=origin_id,destination_id=destination_id,duration=duration)
            db.session.add(flight)
            print(f"Flight successfully added!")
        db.session.commit()

class Passenger(db.Model):
    __tablename__="passengers"
    id = db.Column(db.Integer,primary_key=True)
    fname  = db.Column(db.String,nullable=False)
    lname  = db.Column(db.String,nullable=False)
    gender = db.Column(db.String,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    flight_id = db.Column(db.Integer,db.ForeignKey("flights.id"),nullable=False)

    def preload_passengers():
        f = open("passengers.csv")
        reader = csv.reader(f)
        for fname,lname,gender,age,flight_id in reader:
            p = Passenger(fname=fname,lname=lname,gender=gender,age=age,flight_id=flight_id)
            db.session.add(p)
            print(f"Passenger: {fname} {lname} is successfully added!")
        db.session.commit()

class Airport(db.Model):
    __tablename__ = "airports"
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String,nullable=False)
    country = db.Column(db.String,nullable=False)
    airport_code = db.Column(db.String,nullable=False)

    def preload_airports():
        f = open("airports.csv")
        reader = csv.reader(f)
        for city,country,airport_code in reader:
            a = Airport(city=city,country=country,airport_code=airport_code)
            db.session.add(a)
            print(f"Added airport {city},{country} ({airport_code})")
        db.session.commit()

def main():
    passengers = meta.tables['passengers']
    flights = meta.tables['flights']
    airports = meta.tables['airports']
    passengers.drop()
    flights.drop()
    airports.drop()
    db.create_all()
    Airport.preload_airports()
    Flight.preload_flights()
    Passenger.preload_passengers()

if __name__=="__main__":
    with app.app_context():
        main()
