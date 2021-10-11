import sys
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = 'ebbeb9d031a344878ac299f009ef5a27'
os.environ["SPOTIPY_CLIENT_SECRET"]='89be84be843e4627be7f5292846ecfd0'
os.environ["SPOTIPY_REDIRECT_URI"]='http://localhost:8888/callback'
id = "https://open.spotify.com/playlist/1t6sBuZrFpwsF80UYv9bes?si=a66ac181f06f4e45"

def authcode():
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp

def playlistitems(sp,id):
    start = 0
    total = 1
    anaylsis = []
    while start < total:
        uri = []
        names = sp.playlist_items(id,offset=start)
        total = names["total"]
        for y in range(len(names["items"])):
            uri.append(names["items"][y]["track"]["uri"])
        features = sp.audio_features(uri)
        for x in features:
            l = {}
            r = 0
            for k in ["uri","danceability","energy","speechiness","acousticness","instrumentalness","valence","liveness","tempo"]:
                if k == "uri":
                    l[k] = x[k]
                elif k == "tempo":
                    if int(x[k]) > 108:
                        l[k] = "high"
                    else:
                        l[k] = "low"
                elif float(x[k]) > 0.5:
                    l[k] = "high"
                else:
                    l[k] = "low"
            anaylsis.append(l)
        start += 100
    return anaylsis
def sepration(track_list):
    danceability = { "high" : [] , "low" : [] }
    energy = { "high" : [] , "low" : [] }
    speechiness = { "high" : [] , "low" : [] }
    acousticness = { "high" : [] , "low" : [] }
    instrumentalness = { "high" : [] , "low" : [] }
    valence = { "high" : [] , "low" : [] }
    liveness = { "high" : [] , "low" : [] }
    tempo = { "high" : [] , "low" : [] }


sp = authcode()
tr = playlistitems(sp,id)
print(len(tr))
