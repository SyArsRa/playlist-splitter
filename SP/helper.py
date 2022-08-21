import sys
import os
from dotenv import load_dotenv
from json import loads , dumps
import requests
from urllib.parse import quote
from SP.cluster import cluster

"""Important Variable Declarations for api"""
load_dotenv()
os.environ["SPOTIPY_CLIENT_ID"] = 'ebbeb9d031a344878ac299f009ef5a27'

"""Global Variable Declarations"""
categories = ["danceability","energy","speechiness","acousticness","instrumentalness","valence","liveness","tempo"]

"""Class that stores every song in the playlist_items"""
class song:
    def __init__(self,id,danceability,energy,speechiness,acousticness,instrumentalness,valence,liveness,tempo,name,artist,image):
        self.id = id
        self.danceability = danceability
        self.energy = energy
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.liveness = liveness
        self.tempo = tempo
        self.name = name
        self.artist = artist
        self.image = image

"""function to get authentication from Spotfiy to usee their api"""
def authcode():
    scope = 'playlist-read-private playlist-modify-public playlist-modify-private'
    payload = {
        'client_id': os.environ.get("SPOTIPY_CLIENT_ID"),
        'response_type': 'code',
        'redirect_uri': os.environ.get("SPOTIPY_REDIRECT_URI"),
        'scope': scope,
        }
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in payload.items()])
    auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url_args)
    return auth_url

def tokens(code):
    payload = {
        "grant_type": "authorization_code",
        "code": str(code),
        "redirect_uri": os.environ.get("SPOTIPY_REDIRECT_URI"),
        'client_id': os.environ.get("SPOTIPY_CLIENT_ID"),
        'client_secret': os.environ.get("SPOTIPY_CLIENT_SECRET"),
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=payload)
    return loads(response.text)

def Header(token):
    return  {
             "Accept" : "application/json",
             "Content-Type": "application/json",
             "Authorization": "Bearer {}".format(token['access_token'])
            }

"""Returns Users Playlists"""
def playlists(token):
    headers = Header(token)
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    response = loads(response.text)
    return response['items']

"""extracts playlist from spotify api and then extracts their various characteristics
(important note - playlist_items method on gets first 100 songs from playlist) and return a list of object song with each
object storing a important informations about songs"""
def playlistItems(playlistURL,token):
    global categories

    if "https://open.spotify.com/playlist/" in playlistURL:
        playlistURL = playlistURL.split("/")
        playlistURL = playlistURL[-1].split("?")
        playlistURL = playlistURL[0]

    start = 0
    total = 1
    playlist = []

    while start < total:
        uri = []
        titles = {}
        artist = {}
        images = {}
        headers = Header(token)
        names = requests.get(f"https://api.spotify.com/v1/playlists/{playlistURL}/tracks?offset={start}",headers=headers)
        names = loads(names.text)
        total = names["total"]
        for y in range(len(names["items"])):
            uri.append(names["items"][y]["track"]["id"])
            titles[names["items"][y]["track"]["uri"]] = names["items"][y]["track"]["name"]
            images[names["items"][y]["track"]["uri"]] = names["items"][y]["track"]["album"]["images"][0]["url"]
            art = []
            div = ","
            iteration = len(names["items"][y]["track"]["artists"])

            for artists in names["items"][y]["track"]["artists"]:

                if iteration == 1 :
                    div = ""

                art.append(artists["name"] + div)
                iteration -= 1
            artist[names["items"][y]["track"]["uri"]] = art

        uri = ','.join(uri)
        features = requests.get(f"https://api.spotify.com/v1/audio-features?ids={uri}",headers=headers)
        features = loads(features.text)

        for track in features['audio_features']:
            data = [track[stat] for stat in categories]

            analyzed = song(track["uri"],data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],titles[track["uri"]],artist[track["uri"]],images[track["uri"]])
            playlist.append(analyzed)

        start += 100
    return playlist

"""function that creates kmeans machine learning model  which takes features of a song
and groups them together based on these features"""
def sepration(tracklist):
    groups = cluster(tracklist)
    table = {}
    groups = list(map(lambda x: str(x),groups))

    for song , group in zip(tracklist,groups):
            if group not in table:
                table[group] = [song]
            else:
                table[group] += [song]
    return table

"""Function to convert object song to json"""
def objToDict(song):
    return song.__dict__

"""Function to convert a json formated data back to obj song type"""
def jsonToObj(json):
    return song(json["id"],json["danceability"],json["energy"],json["speechiness"],json["acousticness"],json["instrumentalness"],json["valence"],json["liveness"],json["tempo"],json["name"],json["artist"],json["image"])

"""returns Current User Id"""
def me(token):
    headers = Header(token)
    me = requests.get("https://api.spotify.com/v1/me",headers=headers)
    me = loads(me.text)
    return me["id"]

"""Function used to create playlist on Spotify for users"""
def createPlaylist(cluster,songs,token,userId):
    payload = {
        "name" : ("Sliced Playlist " + cluster),
        "public" : False,
        "description" : "Sliced Playlist " + cluster
    }

    headers = Header(token)
    playlistId = requests.post(f"https://api.spotify.com/v1/users/{userId}/playlists",data=dumps(payload),headers=headers)
    playlistId = loads(playlistId.text)
    playlistId['uri'] = playlistId['uri'].split(":")

    ids = [song.id for song in songs]
    start = 0
    # if list has more than 100 songs loop will unitl less than hundred song are remaining
    if len(ids) > 100:
        while (start + 100) <= len(ids):
            payload = {
                "uris": ids[start:start+100]
                }
            requests.post(f"https://api.spotify.com/v1/playlists/{playlistId['uri'][2]}/tracks",data=dumps(payload),headers=headers)
            start += 100

    payload = {
        "uris": ids[start:len(ids)]
        }
    requests.post(f"https://api.spotify.com/v1/playlists/{playlistId['uri'][2]}/tracks",data=dumps(payload),headers=headers)
