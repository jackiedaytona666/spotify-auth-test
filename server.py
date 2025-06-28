from flask import Flask, request, redirect, render_template
import urllib.parse, os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

load_dotenv()
app = Flask(__name__)

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8889/callback")
SCOPE = "user-top-read user-read-recently-played"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

@app.route("/")
def home():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "❌ No code found in callback.", 400

    try:
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info["access_token"]
        with open("token.txt", "w") as f:
            f.write(access_token)
        print("✅ Access token saved.")
        sp = spotipy.Spotify(auth=access_token)
        user = sp.current_user()
        print("🎧 Logged in as:", user["display_name"])
        return render_template("success.html") if os.path.exists("templates/success.html") else "✅ Login complete."
    except Exception as e:
        print("❌ Error during token exchange:", e)
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(port=8889, debug=True)