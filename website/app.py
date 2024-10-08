from AppleScraper import GetAlbum as GetAppleMusic
from SpotifyScraper import GetAlbum as GetSpotify
from SoundcloudScraper import GetAlbum as GetSoundcloud

from flask import Flask, jsonify, render_template, request, session, url_for
from markupsafe import escape
from werkzeug.utils import redirect


app = Flask(__name__)
app.secret_key = "randomthingeventually"


@app.route("/")
def home_page():
    if "template" not in session:
        session["template"] = "template1"

    return render_template("index.html")


# add an oauth or capcha to use the search


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        alb = {}
        choice = request.form.get("ScrapeOption")
        searchTerm = str(escape(request.form["album_search"]))
        if not choice:
            return home_page()

        if choice == "Spotify":
            alb = GetSpotify(searchTerm)
        if choice == "Apple Music":
            alb = GetAppleMusic(searchTerm)
        if choice == "Soundcloud":
            alb = GetSoundcloud(searchTerm)

        session["album"] = alb
        session.modified = True

        return redirect(url_for("found"))
    else:
        return home_page()


@app.route("/found", methods=["GET", "POST"])
def found():
    # if searching a new album after finding one
    if request.method == "POST":
        return search()

    alb = session.get("album")

    tem = request.form.get("template-selector")
    if tem:
        session["template"] = tem

    template = session["template"]
    return render_template(
        f"{template}.html",
        name=alb["name"],
        artist=alb["artist"],
        year=alb["year"],
        cover=alb["cover"],
        songs=alb["songs"],
    )


app.run(debug=True)
