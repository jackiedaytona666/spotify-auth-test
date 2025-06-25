import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# === Spotify OAuth Setup ===
# === Manual Access Token Debug Mode ===
manual_token = "PASTE_YOUR_ACCESS_TOKEN_HERE"
sp = spotipy.Spotify(auth=manual_token)

print("🔍 Testing token...")
try:
    user = sp.current_user()
    print("✅ Token is valid! Logged in as:", user["display_name"])
except Exception as e:
    print("❌ Token is invalid or expired:", e)
    exit()

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id='34bbf8335e384fe191cec9c8827adf4f',
#     client_secret='826fec361234469e8538d9b1189a7291',
#     redirect_uri='https://jackiedaytona666.github.io/spotify-auth-test/callback.html',
#     scope='user-top-read'
# ))
# === Define Time Ranges ===
timeframes = {
    '1_month': 'short_term',
    '6_months': 'medium_term',
    '2_years': 'long_term'
}

# === Extract and Save Top Tracks and Artists ===
for label, range_key in timeframes.items():
    # Top Tracks
    track_results = sp.current_user_top_tracks(limit=25, time_range=range_key)
    top_tracks = []
    for track in track_results['items']:
        features = None
        try:
            features = sp.audio_features([track['id']])[0]
        except:
            print(f"⚠️ Failed to get audio features for {track['name']}")

        if features:
            top_tracks.append({
                'title': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'valence': features['valence'],
                'energy': features['energy'],
                'danceability': features['danceability'],
                'acousticness': features['acousticness'],
                'instrumentalness': features['instrumentalness'],
                'tempo': features['tempo'],
                'speechiness': features['speechiness'],
                'time_range': label
            })
    pd.DataFrame(top_tracks).to_csv(f'top_tracks_{label}.csv', index=False)

    # Top Artists
    artist_results = sp.current_user_top_artists(limit=25, time_range=range_key)
    top_artists = [{
        'name': artist['name'],
        'genres': ', '.join(artist['genres']),
        'followers': artist['followers']['total'],
        'popularity': artist['popularity'],
        'time_range': label
    } for artist in artist_results['items']]
    pd.DataFrame(top_artists).to_csv(f'top_artists_{label}.csv', index=False)

print("✅ All top tracks and artists saved for 1 month, 6 months, and 2 years.")