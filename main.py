from http import client
import os
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
import json

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

saved_tracks = sp.current_user_saved_tracks()

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

    # print(track['track'])
    # print('\n')
    
    with open('tracks.csv', 'a') as f:
        f.write(f"{id},{name},{duration_ms},{explicit},{popularity}\n")
    with open('artists.csv', 'a') as f:
        f.write(f"{artists_id},{artists_name}\n")
    with open('album.csv', 'a') as f:
        f.write(f"{album_id},{album_name},{album_type},{album_release_date},{album_release_date_precision},{album_number_of_tracks}\n")


# playlists = sp.user_playlists(user="12180975548")
# for playlist in playlists['items']:
#     print(playlist['name'])
#     print(playlist)
#     print("\n")

# temp_playlist = sp.playlist(playlist_id="2VgAYZyszoVQMw0TznVlap")
# print(temp_playlist['tracks']['total'])


# offset = 0
# temp_playlist_tracks = sp.playlist_items(playlist_id="2VgAYZyszoVQMw0TznVlap", offset=offset)
# while(len(temp_playlist_tracks['items']) == 100):
#     for track in temp_playlist_tracks['items']:
#         print(track['track']['name'], ": ", track['track']['id'])

#     offset += 100
#     temp_playlist_tracks = sp.playlist_items(playlist_id="2VgAYZyszoVQMw0TznVlap", offset=offset)


