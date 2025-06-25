from flask import Flask, request, redirect, render_template
import urllib.parse, os

app = Flask(__name__)

CLIENT_ID = "d17e2e495f064737939cbbfb68642d6b"
REDIRECT_URI = "http://127.0.0.1:8889/callback"
SCOPE = "user-top-read"

@app.route("/")
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=token"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&scope={urllib.parse.quote(SCOPE)}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    return render_template("success.html")

@app.route("/save_token", methods=["POST"])
def save_token():
    token = request.json.get("token")
    with open("token.txt", "w") as f:
        f.write(token)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=8889)