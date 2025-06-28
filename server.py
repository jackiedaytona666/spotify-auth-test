from flask import Flask, request, redirect, render_template
import urllib.parse, os, json
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

load_dotenv()
app = Flask(__name__)

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", os.getenv("PUBLIC_URL") + "/callback" if os.getenv("PUBLIC_URL") else "http://127.0.0.1:8889/callback")
SCOPE = "user-top-read user-read-recently-played"

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-auth-url")
def get_auth_url():
    auth_url = sp_oauth.get_authorize_url()
    return {"auth_url": auth_url}


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "❌ No code found in callback.", 400

    try:
        token_info = sp_oauth.get_access_token(code)
        with open(".soul_token.json", "w") as f:
            json.dump(token_info, f)
        print("✅ Token info saved.")
        
        # After successful login, try to get user info
        sp = spotipy.Spotify(auth=token_info["access_token"])
        user = sp.current_user()
        print("🎧 Logged in as:", user["display_name"])
        
        return render_template("success.html") if os.path.exists("templates/success.html") else "✅ Login complete."
    except Exception as e:
        print("❌ Error during token exchange:", e)
        return f"Error: {e}", 500

def get_spotify_token():
    token_info = None
    if os.path.exists(".soul_token.json"):
        with open(".soul_token.json", "r") as f:
            token_info = json.load(f)

    if token_info:
        if sp_oauth.is_token_expired(token_info):
            print("🔄 Token expired, refreshing...")
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            with open(".soul_token.json", "w") as f:
                json.dump(token_info, f)
            print("✅ Token refreshed and saved.")
        else:
            print("✅ Token is valid.")
    else:
        print("⚠️ No token found. Please authorize first.")
    return token_info

# Example of how to use the token (you'll integrate this where you make Spotify API calls)
# @app.route("/some-spotify-data")
# def some_spotify_data():
#     token_info = get_spotify_token()
#     if not token_info:
#         return redirect("/") # Redirect to home for authorization
#     
#     sp = spotipy.Spotify(auth=token_info["access_token"])
#     # Now you can make API calls with 'sp'
#     # For example: sp.current_user_top_artists()
#     return "Data fetched!"

if __name__ == "__main__":
    app.run(port=8889, debug=True)
