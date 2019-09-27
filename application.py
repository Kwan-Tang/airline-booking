from models import *
from flask import Flask,render_template
from sqlalchemy.orm import aliased
from sqlalchemy.sql import functions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    airport_origin = aliased(Airport)
    airport_destination = aliased(Airport)
    flights =  db.session.query(Flight.id,functions.concat(airport_origin.city,", ",airport_origin.country," (",airport_origin.airport_code,")").label("origin") \
                                ,functions.concat(airport_destination.city,", ",airport_destination.country," (",airport_destination.airport_code,")").label("destination") \
                                ,Flight.duration).filter(Flight.origin_id==airport_origin.id).filter(Flight.destination_id==airport_destination.id).all()
    return render_template("index.html",flights=flights)
