import os
import time
import subprocess

TOKEN_PATH = ".soul_token"
SCRIPT_TO_RUN = "spotify_soul_extraction_base.py"

last_modified_time = 0
if os.path.exists(TOKEN_PATH):
    last_modified_time = os.path.getmtime(TOKEN_PATH)

print(f"Watching for changes to {TOKEN_PATH}...")

while True:
    try:
        if os.path.exists(TOKEN_PATH):
            current_modified_time = os.path.getmtime(TOKEN_PATH)
            if current_modified_time != last_modified_time:
                print(f"Token file changed. Running {SCRIPT_TO_RUN}...")
                subprocess.run(["python3", SCRIPT_TO_RUN])
                last_modified_time = current_modified_time
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nWatcher stopped.")
        break
