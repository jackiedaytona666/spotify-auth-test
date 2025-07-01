import os
import json
import requests

TOKEN_PATH = ".soul_token"

# Load token
if not os.path.exists(TOKEN_PATH):
    print("No token found.")
    exit(1)

with open(TOKEN_PATH, "r") as f:
    token_data = json.load(f)

access_token = token_data.get("access_token")
if not access_token:
    print("No access token found.")
    exit(1)

headers = {
    "Authorization": f"Bearer {access_token}"
}

# Test the token by hitting the /me endpoint
profile_res = requests.get("https://api.spotify.com/v1/me", headers=headers)
if profile_res.status_code != 200:
    print(f"Failed to fetch profile data: {profile_res.status_code}")
    print(profile_res.text)  # Add this to debug the exact error message
    exit(1)

print("✅ Profile fetched successfully!")

# Now fetch top artists (1 month as test)
top_artists = requests.get(
    "https://api.spotify.com/v1/me/top/artists?limit=25&time_range=short_term",
    headers=headers
)

if top_artists.status_code != 200:
    print(f"Failed to fetch top artists: {top_artists.status_code}")
    print(top_artists.text)
    exit(1)

# Dump to file
os.makedirs("spotify-soul", exist_ok=True)
with open("spotify-soul/raw_soul_data.json", "w") as out:
    json.dump(top_artists.json(), out, indent=2)

print("✅ Top artists saved to spotify-soul/raw_soul_data.json")