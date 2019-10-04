from models import *
from flask import Flask,render_template,request,jsonify
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
    flight_info = Flight.query.get(flight_id)
    if not flight_info:
        return render_template("error.html",message="The flight does not exist!")
    flight_info.add_passenger(first_name,last_name,gender,age)
    return render_template("success.html")

@app.route("/flights")
def flights():
    flights = retrieve_flights()
    return render_template("flights.html",flights=flights)

@app.route("/airports")
def airports():
    airports = Airport.query.all()
    return render_template("airports.html",airports=airports)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    airport_origin = aliased(Airport)
    airport_destination = aliased(Airport)
    flight_info = Flight.query.get(flight_id)
    flight  = db.session.query(Flight.id
                                ,functions.concat(airport_origin.city," (",airport_origin.airport_code,")").label('origin')
                                ,functions.concat(airport_destination.city," (",airport_destination.airport_code,")").label('destination')
                                ,functions.concat(Flight.duration, " minutes").label('duration'))\
                                .filter(Flight.origin_id==airport_origin.id).filter(Flight.destination_id==airport_destination.id).filter(Flight.id==flight_id).all()
    return render_template("flight.html",flight=flight[0],passengers=flight_info.passengers)

def retrieve_flights():
    airport_origin = aliased(Airport)
    airport_destination = aliased(Airport)
    flights =  db.session.query(Flight.id,functions.concat(airport_origin.city,", ",airport_origin.country," (",airport_origin.airport_code,")").label("origin") \
                                ,functions.concat(airport_destination.city,", ",airport_destination.country," (",airport_destination.airport_code,")").label("destination") \
                                ,Flight.duration).filter(Flight.origin_id==airport_origin.id).filter(Flight.destination_id==airport_destination.id).all()
    return flights

@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error":"Invalid flight_id"}),422
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append({'first_name':passenger.fname,'last_name':passenger.lname,'gender':passenger.gender,'age':passenger.age})
    return jsonify({
                    "id":flight.id
                    ,"origin":[{"city":flight.airport_origin.city,"code":flight.airport_origin.airport_code}]
                    ,"destination":[{"city":flight.airport_destination.city,"code":flight.airport_destination.airport_code}]
                    ,"duration":flight.duration
                    ,"passengers":names
    })
