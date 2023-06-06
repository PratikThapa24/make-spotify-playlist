from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Variables
CLIENT_ID = "your client id "
CLIENT_SECRET = "your client secret"

#Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com/callback/",
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True))

user_id = sp.current_user()['id']


#User Prompt & URl to website
user_response = input("Which year would you like to travel? Type in YYYY-MM-DD format.")
url = f"https://www.billboard.com/charts/hot-100/{user_response}/"
response = requests.get(url=url)
html_text = response.text
year = user_response.split("-")[0]

#Beautiful Soup for Web Scrapping

soup = BeautifulSoup(html_text, "html.parser")
song_title = soup.select("li ul li h3")
songs_list = [song.getText().strip() for song in song_title]
songs_url = []
#Getting the URL for the songs
for title in songs_list:
    result = sp.search(q=f"track:{title} year:{year}", type="track")
    try:
        url = result["tracks"]['items'][0]["uri"]
        songs_url.append(url)
    except IndexError:
        print(f"The {title} is not present in SPOTIFY.")

#Creating a playlist in SPOTIFY
create_playlist = sp.user_playlist_create(user=user_id, name=f"{user_response} Billboard 100", public=False)
# print(songs_url)
#Adding the songs in the created playlist
sp.playlist_add_items(playlist_id=create_playlist["id"], items=songs_url)

