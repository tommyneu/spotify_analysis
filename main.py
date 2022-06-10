import os
import re
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
import database as db

def init_sp():
    load_dotenv()

    # sets environment variables
    scope    = 'user-library-read'
    username = os.environ.get("SPOTIPY_USERNAME")
    cid      = os.environ.get("SPOTIPY_CLIENT_ID")
    secret   = os.environ.get("SPOTIPY_CLIENT_SECRET")
    redirect = os.environ.get("SPOTIPY_REDIRECT_URI")

    # get token and set up spotipy
    token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect)
    if not token:
        print("Token Error")
        exit()
    sp = spotipy.Spotify(auth=token)

    return sp

def init_db():
    load_dotenv()

    neo4j_username = os.environ.get("NEO4J_USERNAME")
    neo4j_password = os.environ.get("NEO4J_PASSWORD")
    neo4j_url      = os.environ.get("NEO4J_URL")

    db.create_connection(neo4j_url, neo4j_username, neo4j_password)



def main():
    init_db()
    sp = init_sp()
    saved_tracks = sp.current_user_saved_tracks(limit=50)

    # TODO: add logic for getting all the saved tracks
    for track in saved_tracks['items']:
        track_id          = track['track']['id']
        track_name        = track['track']['name']
        track_duration_ms = track['track']['duration_ms']
        track_explicit    = track['track']['explicit']
        track_popularity  = track['track']['popularity']

        artists_id   = [artist['id'] for artist in track['track']['artists']]
        artists_name = [artist['name'] for artist in track['track']['artists']]

        album_id                     = track['track']['album']['id']
        album_name                   = track['track']['album']['name']
        album_type                   = track['track']['album']['album_type']
        album_release_date           = track['track']['album']['release_date']
        album_release_date_precision = track['track']['album']['release_date_precision']
        album_number_of_tracks       = track['track']['album']['total_tracks']

        # TODO: any other api calls for data such as artists data and basic track analysis

        db.create_track_node(track_id)
        db.set_track_property(track_id, "name",        track_name)
        db.set_track_property(track_id, "duration_ms", track_duration_ms)
        db.set_track_property(track_id, "explicit",    track_explicit)
        db.set_track_property(track_id, "popularity",  track_popularity)

        db.create_album_node(album_id)
        db.set_album_property(album_id, "name",                   album_name)
        db.set_album_property(album_id, "type",                   album_type)
        db.set_album_property(album_id, "release_date",           album_release_date)
        db.set_album_property(album_id, "release_date_precision", album_release_date_precision)
        db.set_album_property(album_id, "number_of_tracks",       album_number_of_tracks)
        db.connect_nodes("album", album_id, "track", track_id)

        for single_artist_id, single_artist_name in zip(artists_id, artists_name):
            db.create_artist_node(single_artist_id)
            db.set_artist_property(single_artist_id, "name", single_artist_name)
            db.connect_nodes("track", track_id, "artist", single_artist_id)
            db.connect_nodes("album", album_id, "artist", single_artist_id)

        

    db.close_connection()


if __name__ == "__main__":
    main()
    print("finished")

