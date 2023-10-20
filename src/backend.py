from flask import Flask, render_template, request, url_for, flash, redirect
import datetime
import text_to_emoji
import json
import spotify

app = Flask(__name__)  # Initializing flask app


# Route for seeing a data
@app.route("/data")
def get_time():
    x = datetime.datetime.now()
    # Returning an api for showing in  reactjs
    return {"🧾💭🤟🧾🍭": "🧾💭🤟🧾🍭", "🧾💭🤟🧾🍭": "🧾💭🤟🧾🍭", "🧾💭🤟🧾🍭": x, "🧾💭🤟🧾🍭": "🧾💭🤟🧾🍭"}


@app.route("/spotify", methods=["GET", "POST"])
def recive_song_name():
    song_name = request.form["song_name"]
    print(song_name)
    return {"data": {"song_name": song_name}}


@app.route("/spotify_emojis")
def get_emojis():
    for i in recive_song_name():
        song_name = i
        emoji = text_to_emoji.text_to_emoji(song_name)
    return {"data": {"emoji": emoji}}


# Running app
if __name__ == "__main__":
    app.run(debug=True)
