import os
from flask import Flask, redirect, request
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()
import json

# app = Flask(__name__)  # Removed duplicate definition

app = Flask(__name__)

# Automatically bypasses ngrok warning screen after upgrade
@app.after_request
def add_ngrok_skip_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

from flask import Flask
app = Flask(__name__)

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-top-read",
    cache_path="tokens/token.json"
)

@app.route('/')
def home():
    return "Hello, Spotify Soul is running!"

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    return f"Access token saved successfully!<br><br>{access_token}"