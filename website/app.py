from webscraper import GetAlbum
from flask import Flask, render_template, request
from markupsafe import escape



app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        alb = GetAlbum(escape(request.form['album_search']))
        return render_template('poster.html' , name=alb['name'] , artist=alb['artist'], year=alb['year'], cover=alb['cover'],songs=alb['songs'])
    
    return hello_world()

app.run(debug=True)