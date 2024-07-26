from webscraper import GetAlbum
from flask import Flask
from flask import render_template
from markupsafe import escape



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<div>Hi</div>"

@app.route("/search/<searchterm>")
def search(searchterm):
    alb = GetAlbum(escape(searchterm))
    return render_template('poster.html' , name=alb['name'] , artist=alb['artist'], year=alb['year'], cover=alb['cover'],songs=alb['songs'])