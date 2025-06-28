import os
import json
import requests
from datetime import datetime

TOKEN_PATH = ".soul_token"
OUTPUT_DIR = "spotify-soul/house_of_fortunes"

TIME_RANGES = ["short_term", "medium_term", "long_term"]
LIMIT = 25
RECENT_TRACKS_LIMIT = 10

# Read token
if not os.path.exists(TOKEN_PATH):
    print("No token found.")
    exit()

with open(TOKEN_PATH, "r+") as token_file:
    token = token_file.read().strip()
    if token.endswith("✅"):
        print("Token already used.")
        exit()

    headers = {"Authorization": f"Bearer {token}"}

    # Fetch profile data
    profile_resp = requests.get("https://api.spotify.com/v1/me", headers=headers)
    if profile_resp.status_code != 200:
        print(f"Failed to fetch profile data: {profile_resp.status_code}")
        exit()

    profile_data = profile_resp.json()
    user_id = profile_data.get("id", "unknown_user")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{timestamp}_{user_id}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Prepare soul data structure
    soul_data = {
        "profile": profile_data,
        "top_artists": {},
        "top_tracks": {},
        "recent_tracks": {}
    }

    # Fetch top artists and tracks
    for term in TIME_RANGES:
        artists_url = f"https://api.spotify.com/v1/me/top/artists?limit={LIMIT}&time_range={term}"
        tracks_url = f"https://api.spotify.com/v1/me/top/tracks?limit={LIMIT}&time_range={term}"

        artist_resp = requests.get(artists_url, headers=headers)
        track_resp = requests.get(tracks_url, headers=headers)

        if artist_resp.status_code == 200:
            soul_data["top_artists"][term] = artist_resp.json()
        else:
            print(f"Failed to fetch top artists ({term}): {artist_resp.status_code}")

        if track_resp.status_code == 200:
            soul_data["top_tracks"][term] = track_resp.json()
        else:
            print(f"Failed to fetch top tracks ({term}): {track_resp.status_code}")

    # Fetch recently played tracks
    recent_url = f"https://api.spotify.com/v1/me/player/recently-played?limit={RECENT_TRACKS_LIMIT}"
    recent_resp = requests.get(recent_url, headers=headers)
    if recent_resp.status_code == 200:
        soul_data["recent_tracks"] = recent_resp.json()
    else:
        print(f"Failed to fetch recent tracks: {recent_resp.status_code}")

    # Save everything
    if os.path.exists(OUTPUT_DIR) and not os.path.isdir(OUTPUT_DIR):
        os.remove(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(output_path, "w") as out_file:
        json.dump(soul_data, out_file, indent=2)

    # Mark token as used
    token_file.seek(0)
    token_file.write(token + " ✅")
    token_file.truncate()

print(f"🧠 Full soul data saved to {output_path}")