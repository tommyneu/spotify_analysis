# Installation 🔧

Install python and pip

Run `pip install -r requirements.txt` to install packages

Duplicate the `sample.env` file to `.env` and fill it in with your data from the spotify api

🔗[(SPOTIFY API)](https://developer.spotify.com/dashboard/login)
[(SPOTIPY DOCS TOKEN)](https://spotipy.readthedocs.io/en/2.6.1/#authorization-code-flow)

Run `python main.py` to get the data

# First Time Running 🏃

Make sure your spotify redirect URI set to *http://localhost* in the dashboard and in the .env file

When it runs the first time it will open a webpage and prompt you to copy and paste the URL you were taken to

# Functionality 🔨

When run it will output all the relevant data about
a users saved tracks and will output it as CSV files

# Wish List 🎂

- Placing data into a database
- Analyzing data from songs
- Placing songs into playlists