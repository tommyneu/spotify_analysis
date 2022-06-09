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



def main():
    sp = init_sp()
    # saved_tracks = sp.current_user_saved_tracks(limit=50)


    # TODO: add logic for getting all the saved tracks
    # for track in saved_tracks['items']:
    #     id          = track['track']['id']
    #     name        = track['track']['name']
    #     duration_ms = track['track']['duration_ms']
    #     explicit    = track['track']['explicit']
    #     popularity  = track['track']['popularity']

    #     artists_id   = [artist['id'] for artist in track['track']['artists']]
    #     artists_name = [artist['name'] for artist in track['track']['artists']]

    #     album_id                     = track['track']['album']['id']
    #     album_name                   = track['track']['album']['name']
    #     album_type                   = track['track']['album']['album_type']
    #     album_release_date           = track['track']['album']['release_date']
    #     album_release_date_precision = track['track']['album']['release_date_precision']
    #     album_number_of_tracks       = track['track']['album']['total_tracks']

        # TODO: any other api calls for data such as artists data and basic track analysis

        # TODO: store in database



if __name__ == "__main__":
    main()
    print("finished")

    neo4j_username = os.environ.get("NEO4J_USERNAME")
    neo4j_password = os.environ.get("NEO4J_PASSWORD")
    neo4j_url      = os.environ.get("NEO4J_URL")

    db.create_connection(neo4j_url, neo4j_username, neo4j_password)
    db.create_track_node(135)
    result = db.get_track_node(135)
    print(result)
    result = db.set_track_property(135, "value", 454)
    print(result)
    db.delete_track_node(135)

    db.create_album_node(145)
    result = db.get_album_node(145)
    print(result)
    result = db.set_album_property(145, "value", 675)
    print(result)
    db.delete_album_node(145)

    db.create_artist_node(255)
    result = db.get_artist_node(255)
    print(result)
    result = db.set_artist_property(255, "value", 876)
    print(result)
    db.delete_artist_node(255)


    db.close_connection()

