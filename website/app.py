from AppleScraper import GetAlbum as GetAppleMusic
from SpotifyScraper import GetAlbum as GetSpotify
from flask import Flask, render_template, request
from markupsafe import escape



app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

# add an oauth or capcha to use the search

@app.route('/', methods=['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        alb = GetSpotify(escape(request.form['album_search']))
        return render_template('poster.html',
            name=alb['name'],
            artist=alb['artist'],
            year=alb['year'],
            cover=alb['cover'],
            songs=alb['songs'])

    return home_page()

app.run(debug=True)
