# Spotify to Last.fm - Transfer Liked Songs Script

This Python script allows you to transfer your liked songs from Spotify to your Last.fm account as "loved" tracks. The script logs the transferred likes, allowing you to rerun it periodically to update recent likes. It will continue until it encounters likes that have already been logged. It helps you synchronize your music preferences between the two platforms by automating the process.

## Features

- **Automatic Transfer**: The script automatically transfers your liked songs from Spotify to Last.fm.
- **Automatic Updates**: It keeps a log of already transferred songs and stops once the transfered likes are up to date.
- **Clean Titles**: Strips release markers like `- 2014 Remaster`, `(Deluxe Edition)` or `(Explicit)` before loving, so the love lands on the same Last.fm track your scrobbles use instead of a separate, album-less entry. Set `CLEAN_TITLES = False` to love Spotify's exact titles.
- **Customizable Limit**: You can optionally set a limit on the number of songs to transfer. It will always start transferring the most recent likes.

## Prerequisites

Before you begin, ensure you have the following:

1. **Python 3.x**: The script requires Python 3.x to run. You can download Python from [python.org](https://www.python.org/downloads/).
2. **Spotify Developer Account**: You need to create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to get your Client ID and Client Secret.
3. **Last.fm API Key**: Create a developer account and generate an API key on the [Last.fm API page](https://www.last.fm/api).

## Installation Guide

Follow these steps to set up and run the script:

### 1. Clone the Repository

First, download or clone the repository:

```bash
git clone https://github.com/RaphaelMaschinsen/SpotifyLikesToLastfm.git
cd SpotifyLikesToLastfm
```

### 2. Install Required Python Packages

You can install all required Python packages using the `requirements.txt` file. Open a terminal or command prompt and run:

```bash
pip install -r requirements.txt
```

### 3. Set Up Your Spotify and Last.fm Credentials

#### Spotify App Configuration

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in.
2. Create a new app by clicking the "Create an App" button.
3. Fill in the required details for your app.
4. After creating the app, you'll see a section called **Redirect URIs**.
5. Add `http://localhost:8888/callback` as a redirect URI. This is necessary because the script uses this address to receive the authentication token from Spotify.
6. Save your changes and note down your **Client ID** and **Client Secret**.

#### Last.fm Developer Account Setup

1. Visit the [Last.fm API page](https://www.last.fm/api).
2. Log in with your Last.fm account or create one if you don’t have it.
3. Click on the "Get an API account" link.
4. Fill in the form with any app name (it can be anything, like "Spotify to Last.fm Transfer").
5. After submitting the form, you’ll receive your **API Key** and **Shared Secret**.

#### Configure the Script

Open the script (`main.py`) in a text editor and replace the placeholder values with your actual credentials:

```python
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # This should match the URI configured in your Spotify app
LASTFM_API_KEY = 'your_lastfm_api_key'
LASTFM_API_SECRET = 'your_lastfm_api_secret'
LASTFM_USERNAME = 'your_lastfm_username'
LASTFM_PASSWORD = 'your_lastfm_password'
```

### 4. Run the Script

Once you have set up your credentials, you can run the script:

```bash
python main.py
```

The script will start transferring your liked songs from Spotify to Last.fm. It will log each transferred song and stop if it encounters a song that has already been transferred.

### 5. Customize the Script

You can customize the script by setting a limit on the number of songs to transfer (the default is 'None' so it will transfer all liked songs):

```python
LIMIT_NUMBER_OF_RECENT_LIKES_TO_TRANSFER = 100  # Set to None to transfer all liked songs
```

### 6. View Logs

The script creates a log file (`loved_songs.log`) where it records the songs that have been transferred.

## Contributing

If you want to contribute to this project, feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.

## Notes

- Make sure to update the sections where placeholders like `'yourusername'`, `'your_spotify_client_id'`, `'your_spotify_client_secret'`, etc., are used with the actual details.
- This README assumes a basic level of understanding of using a terminal/command prompt and running Python scripts, which should be accessible to users with minimal Python experience.
