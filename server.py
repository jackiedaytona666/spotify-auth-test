import os
import json
import time
from flask import Flask, redirect, request, jsonify, render_template
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
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

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed."

    cache_path = f".cache-{int(time.time())}"

    sp_oauth_instance_for_callback = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read user-read-recently-played",
        cache_path=cache_path
    )

    token_info = sp_oauth_instance_for_callback.get_access_token(code, as_dict=True)

    if token_info:
        try:
            with open(cache_path, 'w') as f:
                json.dump(token_info, f, indent=4)
            print(f"[+] Token explicitly saved to {cache_path}")
        except Exception as e:
            print(f"[-] Error saving token to {cache_path}: {e}")

        return redirect("/exit")
    else:
        return "Failed to get access token."

@app.route('/api/soul', methods=['GET'])
def get_soul_data():
    soul_path = 'path/raw_soul_data.json'

    if not os.path.exists(soul_path):
        return jsonify({"error": "Soul data not found"}), 404

    with open(soul_path, 'r') as f:
        soul_data = json.load(f)

    return jsonify(soul_data)

@app.route('/get-auth-url')
def get_auth_url():
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({'auth_url': auth_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8889, debug=True)