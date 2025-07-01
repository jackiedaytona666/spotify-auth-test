import os
import json
import requests
from datetime import datetime

TOKEN_PATH = ".soul_token"
OUTPUT_DIR = "spotify-soul/house_of_fortunes"
PROCESSED_DIR = "spotify-soul/house_of_fortunes/souls_who_passed_on"
FILE_LIST_PATH = "spotify-soul/pending_tokens.json"

# Load list of tokens
if not os.path.exists(FILE_LIST_PATH):
    print("No pending token list found.")
    exit()

with open(FILE_LIST_PATH, "r") as f:
    token_list = json.load(f)

if not token_list:
    print("No tokens to process.")
    exit()

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

for token_obj in token_list:
    token = token_obj.get("token")
    if not token or token.endswith("✅"):
        continue

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch profile data for token: {response.status_code}")
        continue

    profile_data = response.json()
    user_id = profile_data.get("id", "unknown_user")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{timestamp}_{user_id}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, "w") as out_file:
        json.dump(profile_data, out_file, indent=2)

    # Move the used file to souls_who_passed_on
    processed_path = os.path.join(PROCESSED_DIR, output_filename)
    os.rename(output_path, processed_path)

    print(f"✅ Processed and archived: {processed_path}")