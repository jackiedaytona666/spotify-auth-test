import os
import json
import requests
from datetime import datetime

TOKEN_PATH = ".soul_token"
OUTPUT_DIR = "spotify-soul/house_of_fortunes"

# Read token
if not os.path.exists(TOKEN_PATH):
    print("No token found.")
    exit()

with open(TOKEN_PATH, "r+") as token_file:
    token = token_file.read().strip()
    if token.endswith("✅"):
        print("Token already used.")
        exit()

# Fetch user profile data
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.spotify.com/v1/me", headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch profile data: {response.status_code}")
    exit()

profile_data = response.json()
user_id = profile_data.get("id", "unknown_user")
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"{timestamp}_{user_id}.json"
output_path = os.path.join(OUTPUT_DIR, output_filename)

# Save data
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(output_path, "w") as out_file:
    json.dump(profile_data, out_file, indent=2)

# Mark token as used
token_file.seek(0)
token_file.write(token + " ✅")
token_file.truncate()

print(f"Saved profile to {output_path}")