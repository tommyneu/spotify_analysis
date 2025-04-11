# Installation 🔧

Install docker, python, and pip on your machine

Run `python3 -m venv ./venv` to create a venv
Run `venv/bin/pip3 install -r requirements.txt` to install all python modules
Run `venv/bin/python3 main.py` to run main.py

Duplicate **sample.env** file to **.env** and fill it in with your data from the spotify api

🔗[(SPOTIFY API)](https://developer.spotify.com/dashboard/login)
[(SPOTIPY DOCS TOKEN)](https://spotipy.readthedocs.io/en/2.6.1/#authorization-code-flow)

Use `docker-compose up` to build and run the neo4j container
- The data for the database is stored in the directory neo4j
- Credentials for the neo4j database are set in the **.env** file
- You can view the database at [http://localhost:7474](http://localhost:7474)

# First Time Running 🏃

Make sure your spotify redirect URI set to **http://localhost** in the dashboard and in the **.env** file

When it runs the first time it will open a webpage and prompt you to copy and paste the URL you were taken to

# Functionality 🔨

When run it will output all the relevant data about
a users saved tracks and will output into a neo4j database

## Wish List 🎂

- Unit Tests
- Analyzing data from songs
- Placing songs into playlists