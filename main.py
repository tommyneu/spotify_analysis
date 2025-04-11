import os
from time import sleep
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
import database as db
import json
import analysis as an
import subprocess

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


def get_and_store_all_saved_tracks(sp):
    offset = 0
    max_limit_saved_tracks = 50
    saved_tracks = sp.current_user_saved_tracks(limit=max_limit_saved_tracks, offset=offset)

    while len(saved_tracks['items']) > 0:
        print(f"Tracks: {offset} - {offset + max_limit_saved_tracks}")
        sleep(0.5)

        for track in saved_tracks['items']:
            track_added_at          = track['added_at']

            track_id          = track['track']['id']
            track_name        = track['track']['name']
            track_duration_ms = track['track']['duration_ms']
            track_explicit    = track['track']['explicit']
            track_popularity  = track['track']['popularity']
            track_href        = track['track']['external_urls']['spotify']

            artists_id   = [artist['id'] for artist in track['track']['artists']]
            artists_name = [artist['name'] for artist in track['track']['artists']]

            album_id                     = track['track']['album']['id']
            album_name                   = track['track']['album']['name']
            album_type                   = track['track']['album']['album_type']
            album_release_date           = track['track']['album']['release_date']
            album_release_date_precision = track['track']['album']['release_date_precision']
            album_number_of_tracks       = track['track']['album']['total_tracks']
            album_artists_id             = [artist['id'] for artist in track['track']['album']['artists']]
            album_artists_name           = [artist['name'] for artist in track['track']['album']['artists']]

            # print(json.dumps(track, sort_keys=True, indent=2))
            # print("")
            # print("")

            # TODO: any other api calls for data such as artists data and basic track analysis

            db.create_track_node(track_id)
            db.set_track_property(track_id, "name",        track_name)
            db.set_track_property(track_id, "duration_ms", track_duration_ms)
            db.set_track_property(track_id, "explicit",    track_explicit)
            db.set_track_property(track_id, "popularity",  track_popularity)
            db.set_track_property(track_id, "href",        track_href)
            db.set_track_datetime(track_id, track_added_at)

            db.create_album_node(album_id)
            db.set_album_property(album_id, "name",                   album_name)
            db.set_album_property(album_id, "type",                   album_type)
            db.set_album_property(album_id, "release_date_precision", album_release_date_precision)
            db.set_album_property(album_id, "number_of_tracks",       album_number_of_tracks)
            db.set_album_datetime(album_id, album_release_date)
            db.connect_nodes("album", album_id, "track", track_id)

            for single_artist_id, single_artist_name in zip(album_artists_id, album_artists_name):
                db.create_artist_node(single_artist_id)
                db.set_artist_property(single_artist_id, "name", single_artist_name)
                db.connect_nodes("album", album_id, "artist", single_artist_id)

            for single_artist_id, single_artist_name in zip(artists_id, artists_name):
                db.create_artist_node(single_artist_id)
                db.set_artist_property(single_artist_id, "name", single_artist_name)
                db.connect_nodes("track", track_id, "artist", single_artist_id)

        offset += max_limit_saved_tracks
        saved_tracks = sp.current_user_saved_tracks(limit=max_limit_saved_tracks, offset=offset)

def get_and_store_audio_features_of_all_tracks(sp):
    tracks_data = db.get_all_track_nodes()
    tracks = [track['t']['id'] for track in tracks_data]
    max_limit_audio_features = 100

    for index in range(0, len(tracks), max_limit_audio_features):
        sleep(0.5)
        print(f"Audio Features: {index} - {index+max_limit_audio_features}")
        tracks_subset = tracks[index:index+max_limit_audio_features]
        results = sp.audio_features(tracks_subset)

        for track in results:
            id               = track['id']
            danceability     = track['danceability']
            energy           = track['energy']
            key              = track['key']
            loudness         = track['loudness']
            mode             = track['mode']
            speechiness      = track['speechiness']
            acousticness     = track['acousticness']
            instrumentalness = track['instrumentalness']
            liveness         = track['liveness']
            valence          = track['valence']
            tempo            = track['tempo']
            time_signature   = track['time_signature']

            db.set_track_property(id, "danceability",     danceability)
            db.set_track_property(id, "energy",           energy)
            db.set_track_property(id, "key",              key)
            db.set_track_property(id, "loudness",         loudness)
            db.set_track_property(id, "mode",             mode)
            db.set_track_property(id, "speechiness",      speechiness)
            db.set_track_property(id, "acousticness",     acousticness)
            db.set_track_property(id, "instrumentalness", instrumentalness)
            db.set_track_property(id, "liveness",         liveness)
            db.set_track_property(id, "valence",          valence)
            db.set_track_property(id, "tempo",            tempo)
            db.set_track_property(id, "time_signature",   time_signature)

def get_and_store_artist_data_of_all_artists(sp):
    artist_data = db.get_all_artist_nodes()
    artists = [artist['a']['id'] for artist in artist_data]
    max_limit_artist = 50

    for index in range(0, len(artists), max_limit_artist):
        sleep(0.5)
        print(f"Artists: {index} - {index+max_limit_artist}")
        artists_subset = artists[index:index+max_limit_artist]
        results = sp.artists(artists_subset)

        for artist in results['artists']:
            id         = artist['id']
            followers  = artist['followers']['total']
            genres     = artist['genres']
            popularity = artist['popularity']

            for genre in genres:
                db.create_genre_node(genre)
                db.connect_nodes("artist", id, "genre", genre)
            
            db.set_artist_property(id, "followers",  followers)
            db.set_artist_property(id, "popularity", popularity)

def download_tracks():
    tracks_data = db.get_all_track_nodes()
    tracks = [track['t']['href'] for track in tracks_data]
    max_limit_tracks = 50

    for index in range(0, len(tracks)):
        print(f"Track Download: {index + 1} of {len(tracks)}")
        subprocess.run(['/Users/tneumann9/Documents/Personal Projects/spotify_analysis/venv/bin/spotdl', '--output', './tracks', 'download', tracks[index]])

def main():
    init_db()
    sp = init_sp()

    # get_and_store_all_saved_tracks(sp)
    # get_and_store_audio_features_of_all_tracks(sp)
    # get_and_store_artist_data_of_all_artists(sp)

    results = db.get_all_track_nodes()
    results = [track['t'] for track in results]
    for track in results:
        del track['added_at']
    an.load_data(json.dumps(results))

    # an.plot_data('acousticness', 'danceability')
    an.fcm()

    db.close_connection()


if __name__ == "__main__":
    main()
    print("finished")