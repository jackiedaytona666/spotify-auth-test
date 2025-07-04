import os
import json 
from flask import Flask, redirect, request, jsonify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def entrance():
    return render_template('index.html')

@app.route('/exit')
def exit_screen():
    return render_template('exit.html')

# ngrok bypass warning
@app.after_request
def add_ngrok_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read user-read-recently-played",
    cache_path=".cache"
)

@app.route('/')
def index():
    return "🧠 Spotify Soul Extraction is running."

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed."

    token_info = sp_oauth.get_access_token(code)
    return f"✅ Access token saved. Close this tab. <br><br>{token_info['access_token']}"

@app.route('/api/soul', methods=['GET'])
def get_soul_data():
    soul_path = 'spotify_soul/raw_soul_data.json'

    if not os.path.exists(soul_path):
        return jsonify({"error": "Soul data not found"}), 404

    with open(soul_path, 'r') as f:
        soul_data = json.load(f)

    return jsonify(soul_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8889, debug=True)
