# Installation 🔧

You will need docker, docker-compose, python, and pip on your machine

1. Go to [Spotify API Dashboard](https://developer.spotify.com/dashboard/login) and create a project on your account
   - Make sure to copy the *Client Id* and the *Client Secret*
   - The website URL does not matter I have mine set to `http://localhost`
   - Set the redirect URI to `https://example.com` it just needs to be something valid and secure we don't need to be able to reach it
2. Copy `sample.env` to `.env` (Run `cp ./sample.env ./.env`)
    - Replace values for `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` with what is on that spotify dashboard
    - Your spotify username is probably nothing like your email or name in spotify. Go to settings and account and you will find your actual username. Mine is just a giant number
    - You can keep the Neo4j stuff as the default since it is all local it doesn't really matter
3. Run `python3 -m venv ./venv` to create a python virtual environment
4. Run `venv/bin/pip3 install -r requirements.txt` to install all python modules
5. Use `docker-compose up` to build and run the Neo4j container
    - The data for the database is stored in the directory Neo4j
    - Credentials for the Neo4j database are set in the **.env** file
    - You can view the database at [http://localhost:7474](http://localhost:7474)

## Running it for the first time

When you run it the first time it will open the spotify authentication stuff in your browser. If you have your redirect URI set to `https://example.com` then after you login it will take you to some `https://example.com` page. You will then need to copy that URL it redirected you to into the terminal. That will let the app authenticate you as you and be able to pull your data

## Data Collection

This will pull data related to your liked songs. It will get their name, duration, date liked, and popularity. It will also get the album the song is in, the album release date, the number of tracks on the album, and the type of album (single, compilation, etc.). We will also get the artist who produced, performed or featured in those songs. We will get the artists popularity and genres as well.
