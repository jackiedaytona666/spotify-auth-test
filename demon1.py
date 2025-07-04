import os
import json
import datetime
from flask import Flask, redirect, request
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Load secrets
load_dotenv()

# Config
DEMON_ID = "demon1"
PORT = 8881
REDIRECT_URI = os.getenv("NGROK_REDIRECT_URI")  # Use your full ngrok URL here

# Flask setup
app = Flask(__name__)

# Spotify auth setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=REDIRECT_URI,
    scope="user-top-read user-read-recently-played",
    cache_path=f".cache-{DEMON_ID}"
)

@app.route("/")
def index():
    return f"🧿 {DEMON_ID} is watching the tunnel."

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "💀 No code received. Something broke."

    token_info = sp_oauth.get_access_token(code)
    if not token_info:
        return "☠️ Token exchange failed."

    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)

    # Pull soul data
    soul_data = {
        "tracks": {
            "short_term": sp.current_user_top_tracks(time_range="short_term", limit=25),
            "medium_term": sp.current_user_top_tracks(time_range="medium_term", limit=25),
            "long_term": sp.current_user_top_tracks(time_range="long_term", limit=25)
        },
        "artists": {
            "short_term": sp.current_user_top_artists(time_range="short_term", limit=25),
            "medium_term": sp.current_user_top_artists(time_range="medium_term", limit=25),
            "long_term": sp.current_user_top_artists(time_range="long_term", limit=25)
        },
        "recently_played": sp.current_user_recently_played(limit=10)
    }

    # Save soul
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("spotify_soul", exist_ok=True)
    path = f"spotify_soul/{DEMON_ID}_{timestamp}.json"
    with open(path, "w") as f:
        json.dump(soul_data, f, indent=2)

    return f"✅ {DEMON_ID} caught a soul. File saved to:<br><code>{path}</code><br><br>You may close this window."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

