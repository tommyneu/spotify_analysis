import os
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
from neo4j import GraphDatabase
from neo4j.debug import watch

def init_sp():
    load_dotenv()

    # sets environment variables
    scope    = 'user-library-read'
    username = os.environ.get("SPOTIPY_USERNAME")
    cid      = os.environ.get("SPOTIPY_CLIENT_ID")
    secret   = os.environ.get("SPOTIPY_CLIENT_SECRET")
    redirect = os.environ.get("SPOTIPY_REDIRECT_URI")

    # get token and set up spotipy
    token = util.prompt_for_user_token(username, scope, client_id=cid,client_secret=secret, redirect_uri=redirect)
    if not token:
        print("Token Error")
        exit()
    sp = spotipy.Spotify(auth=token)

    return sp



def main():
    sp = init_sp()
    saved_tracks = sp.current_user_saved_tracks(limit=50)


    # puts the column headings in and removes any data previously in the files
    with open('tracks.csv', 'w') as f:
            f.write(f"id,name,duration_ms,explicit,popularity\n")
    with open('artists.csv', 'w') as f:
        f.write(f"artist_id,artist_name\n")
    with open('album.csv', 'w') as f:
        f.write(f"album_id,album_name,album_type,album_release_date,album_release_date_precision,album_number_of_tracks\n")


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

            # TODO: remove duplicate artists
            for single_artist_id, single_artist_name in zip(artists_id, artists_name):
                f.write(f"{single_artist_id},{single_artist_name}\n")
        with open('album.csv', 'a') as f:
            f.write(f"{album_id},{album_name},{album_type},{album_release_date},{album_release_date_precision},{album_number_of_tracks}\n")


def create_person(tx, name):
    result = tx.run("CREATE (p:Person{name:$name}) RETURN p", name=name).data()
    return result

def get_person(tx, name):
    result = tx.run("MATCH (p:Person) RETURN p", name=name).data()
    return result

if __name__ == "__main__":
    main()
    print("finished")

    uri = "neo4j://neo4j:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

    with driver.session() as session:
        result = session.write_transaction(create_person, "bob")
        print([record for record in result])
        result = session.read_transaction(get_person, "bob")
        print([record for record in result])
        

    driver.close()

