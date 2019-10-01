from models import *
from flask import Flask,render_template,request
from sqlalchemy.orm import aliased
from sqlalchemy.sql import functions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    flights = retrieve_flights()
    return render_template("index.html",flights=flights)

@app.route("/book",methods=["POST"])
def book():
    flight_id = request.form.get("flight_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    gender = request.form.get("gender")
    age = request.form.get("age")
    print(f"Passenger {first_name} {last_name} {gender} {age} booked to flight id {flight_id}.")
    flight_info = Flight.query.get(flight_id)
    if not flight_info:
        return render_template("error.html",message="The flight does not exist!")
    return render_template("success.html")

@app.route("/flights")
def flights():
    flights = retrieve_flights()

    return render_template("flights.html",flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = Flight.query.get(flight_id)
    return render_template("flight.html",flight=flight,passengers=flight.passengers)

def retrieve_flights():
    airport_origin = aliased(Airport)
    airport_destination = aliased(Airport)
    flights =  db.session.query(Flight.id,functions.concat(airport_origin.city,", ",airport_origin.country," (",airport_origin.airport_code,")").label("origin") \
                                ,functions.concat(airport_destination.city,", ",airport_destination.country," (",airport_destination.airport_code,")").label("destination") \
                                ,Flight.duration).filter(Flight.origin_id==airport_origin.id).filter(Flight.destination_id==airport_destination.id).all()
    return flights
