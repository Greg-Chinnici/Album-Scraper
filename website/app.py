from AppleScraper import GetAlbum as GetAppleMusic
from SpotifyScraper import GetAlbum as GetSpotify
from SoundcloudScraper import GetAlbum as GetSoundcloud
from flask import Flask, render_template, request, session
from markupsafe import escape
from Album import Album



app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

# add an oauth or capcha to use the search

@app.route('/', methods=['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        alb = {}
        choice = request.form.get('ScrapeOption')
        if not choice:
            return home_page()
        match choice:
            case "Spotify":
                alb = GetSpotify(escape(request.form["album_search"]))
            case "Apple Music":
                alb = GetAppleMusic(escape(request.form["album_search"]))
            case "Soundcloud":
                alb = GetSoundcloud(escape(request.form["album_search"]))

        return render_template('poster.html',
            name=alb['name'],
            artist=alb['artist'],
            year=alb['year'],
            cover=alb['cover'],
            songs=alb['songs'])

    return home_page()

app.run(debug=True)
