"""
MIT License

Copyright (c) 2024 Raphael Maschinsen
raphaelmaschinsen@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pylast
import os
from typing import Optional

from title_cleaner import clean_title

# Limit how many liked songs you want to transfer (order is starting with the most recent likes)
# Set to None to transfer all liked songs
LIMIT_NUMBER_OF_RECENT_LIKES_TO_TRANSFER: Optional[int] = None
LOG_FILE = 'loved_songs.log'
# Love "Changes" instead of "Changes - 2013 Remaster", so loves land on the track you actually scrobble
CLEAN_TITLES = True

# Replace these with your actual credentials
SPOTIFY_CLIENT_ID = 'SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
LASTFM_API_KEY = 'LASTFM_API_KEY'
LASTFM_API_SECRET = 'LASTFM_API_SECRET'
LASTFM_USERNAME = 'LASTFM_USERNAME'
LASTFM_PASSWORD = 'LASTFM_PASSWORD'

# Step 1: Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope="user-library-read"))

# Step 2: Authenticate with Last.fm
network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
    username=LASTFM_USERNAME,
    password_hash=pylast.md5(LASTFM_PASSWORD),
)

# Function to read log file and get already loved song identifiers
def read_loved_songs_log(file_path: str) -> set:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    return set()

# Function to write a song's details to the log file
def log_loved_song(file_path: str, artist: str, title: str, id_: str):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{artist} - {title} - {id_}\n")

# Load already loved song identifiers from the log file
loved_songs_log = read_loved_songs_log(LOG_FILE)

# Initialize variables for loop
offset = 0
liked_songs_count = 0
encountered_already_loved_song = False

while True:
    # Fetch liked songs in batches of 50
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    liked_songs = results['items']

    if not liked_songs:  # If no more songs are found, break out of the loop
        break

    for item in liked_songs:
        if (
            LIMIT_NUMBER_OF_RECENT_LIKES_TO_TRANSFER is not None and
            liked_songs_count >= LIMIT_NUMBER_OF_RECENT_LIKES_TO_TRANSFER
        ):
            break

        track = item['track']
        track_id = track['id']  # Get the unique track ID
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        song_identifier = f"{artist_name} - {track_name} - {track_id}"

        # Stop the process if the song is already loved
        if song_identifier in loved_songs_log:
            print(f"Encountered already loved song: {track_name} by {artist_name}. Stopping the process.")
            encountered_already_loved_song = True
            break

        lastfm_track_name = clean_title(track_name) if CLEAN_TITLES else track_name
        print(f"Loving {lastfm_track_name} by {artist_name} on Last.fm")

        # Love the song on Last.fm
        track_lfm = network.get_track(artist_name, lastfm_track_name)
        track_lfm.love()

        # Log the song details to the file
        log_loved_song(LOG_FILE, artist_name, track_name, track_id)

        liked_songs_count += 1

    if encountered_already_loved_song or (
        LIMIT_NUMBER_OF_RECENT_LIKES_TO_TRANSFER is not None and
        liked_songs_count >= LIMIT_NUMBER_OF_RECENT_LIKES_TO_TRANSFER
    ):
        break

    # Increase offset to get the next batch of liked songs
    offset += 50

if encountered_already_loved_song:
    print("Stopped because it encountered an already logged liked song.")
else:
    print(f"Done loving {liked_songs_count} liked songs on Last.fm!")
