from models import *
from flask import Flask,render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    flights =  db.session.query(Flight,Airport).filter(Flight.origin_id==Airport.id).all()
    return render_template("index.html",flights=flights)
