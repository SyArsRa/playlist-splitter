import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = 'ebbeb9d031a344878ac299f009ef5a27'
os.environ["SPOTIPY_CLIENT_SECRET"]='89be84be843e4627be7f5292846ecfd0'
os.environ["SPOTIPY_REDIRECT_URI"]='http://localhost:8888/callback'



urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
scope = "playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

artist = sp.artist(urn)
print(artist)
