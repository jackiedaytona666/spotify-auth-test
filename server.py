from flask import Flask, request, redirect, render_template
import urllib.parse, os

app = Flask(__name__)

CLIENT_ID = "d17e2e495f064737939cbbfb68642d6b"
REDIRECT_URI = "http://127.0.0.1:8889/callback"
SCOPE = "user-top-read"

@app.route("/callback")
def callback():
    try:
        with open("token.txt", "r") as f:
            token = f.read().strip()

        import spotipy
        sp = spotipy.Spotify(auth=token)

        print("🔍 Testing token...")
        user = sp.current_user()
        print("✅ Token is valid! Logged in as:", user["display_name"])

        return render_template("success.html")
    except Exception as e:
        print("❌ Token is invalid or expired:", e)
        return f"Error: {e}", 500
