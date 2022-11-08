from bs4 import BeautifulSoup
import requests
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, CLIENT_URI

scope = 'playlist-modify-private'

auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=CLIENT_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)\

current_user_id = sp.current_user()["id"]

user_response = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD: ")


def validate_user_response(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        user_response = input("Sorry, that wasn't type out correctly. Please use this format when entering the date: YYYY-MM-DD: ")
        validate_user_response(user_response)


validate_user_response(user_response)
user_input_year = user_response.split("-")[0]

URL=f"https://www.billboard.com/charts/hot-100/{user_response}/"
response = requests.get(URL)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

results = soup.select("li ul li h3")
names = [result.text.strip() for result in results]

for name in names:
    track = sp.search(q=f"track:{name} year:{user_input_year}", type="track")
    try:
        print(track["tracks"]["items"][0]["uri"])
    except IndexError:
        print("Can't find song on Spotify")
