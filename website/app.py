from webscraper import GetAlbum
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<div>Hi</div>"

@app.route("/search")
def search():
    alb = GetAlbum("beerbongs and bentlys")
    return render_template('poster.html' , name=alb['name'] , artist=alb['artist'], year=alb['year'], cover=alb['cover'])