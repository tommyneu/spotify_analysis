import os
from dotenv import load_dotenv
import spotipy
import spotipy.util as util

load_dotenv()

scope    = 'user-library-read'
username = os.environ.get("SPOTIPY_USERNAME")
cid      = os.environ.get("SPOTIPY_CLIENT_ID")
secret   = os.environ.get("SPOTIPY_CLIENT_SECRET")
redirect = os.environ.get("SPOTIPY_REDIRECT_URI")

token = util.prompt_for_user_token(username, scope, client_id=cid,client_secret=secret, redirect_uri=redirect)

if not token:
    print("Token Error")
    exit()

sp = spotipy.Spotify(auth=token)

saved_tracks = sp.current_user_saved_tracks(limit=50)

# TODO: DELETE the files that are already there
# TODO: add logic for getting all the saved tracks

for track in saved_tracks['items']:
    id          = track['track']['id']
    name        = track['track']['name']
    duration_ms = track['track']['duration_ms']
    explicit    = track['track']['explicit']
    popularity  = track['track']['popularity']

    artists_id   = [artist['id'] for artist in track['track']['artists']]
    artists_name = [artist['name'] for artist in track['track']['artists']]

    album_id                     = track['track']['album']['id']
    album_name                   = track['track']['album']['name']
    album_type                   = track['track']['album']['album_type']
    album_release_date           = track['track']['album']['release_date']
    album_release_date_precision = track['track']['album']['release_date_precision']
    album_number_of_tracks       = track['track']['album']['total_tracks']

    # TODO: any other api calls for data such as artists data and basic track analysis

    with open('tracks.csv', 'a') as f:
        f.write(f"{id},{name},{duration_ms},{explicit},{popularity}\n")
    with open('artists.csv', 'a') as f:
        f.write(f"{artists_id},{artists_name}\n")
    with open('album.csv', 'a') as f:
        f.write(f"{album_id},{album_name},{album_type},{album_release_date},{album_release_date_precision},{album_number_of_tracks}\n")


