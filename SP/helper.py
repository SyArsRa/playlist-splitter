import sys
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json
"""Important Variable Declarations for api"""
load_dotenv()
os.environ["SPOTIPY_CLIENT_ID"] = 'ebbeb9d031a344878ac299f009ef5a27'

"""Global Variable Declarations"""
categories = ["danceability","energy","speechiness","acousticness","instrumentalness","valence","liveness"]

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
def authcode(scope,request):
    cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(request)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("SPOTIPY_CLIENT_ID"),client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
                            redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),scope=scope,cache_handler=cache_handler,show_dialog=True))
    return sp


"""extracts playlist from spotify api and then extracts their various characteristics
(important note - playlist_items method on gets first 100 songs from playlist) and return a list of object song with each
object storing a important informations about songs"""
def playlistItems(playlistURL,request):
    global categories
    start = 0
    total = 1
    playlist = []
    sp = authcode("playlist-read-private",request)
    while start < total:
        uri = []
        titles = {}
        artist = {}
        images = {}
        names = sp.playlist_items(playlistURL,offset=start)
        total = names["total"]
        for y in range(len(names["items"])):
            uri.append(names["items"][y]["track"]["uri"])
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
        features = sp.audio_features(uri)
        for track in features:
            data = ["high" if track[stat] > 0.5 else "low" for stat in categories]
            if int(track["tempo"]) > 108:
                data += ["high"]
            else:
                data += ["low"]
            analyzed = song(track["uri"],data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],titles[track["uri"]],artist[track["uri"]],images[track["uri"]])
            playlist.append(analyzed)
        start += 100
    categories += ["tempo"]
    return playlist

"""function that creates a dict of each characteristics of a song
and stores songs coresspoding to their range in the area and return the dict"""
def sepration(track_list):
    info_list = {
        "danceability" : { "high" : [] , "low" : [] } ,
        "energy" : { "high" : [] , "low" : [] } ,
        "speechiness" : { "high" : [] , "low" : [] } ,
        "acousticness" : { "high" : [] , "low" : [] } ,
        "instrumentalness" : { "high" : [] , "low" : [] } ,
        "valence" : { "high" : [] , "low" : [] } ,
        "liveness" : { "high" : [] , "low" : [] } ,
        "tempo" : { "high" : [] , "low" : [] } ,
           }
    for x in track_list:
        info_list["danceability"][x.danceability].append(x)
        info_list["energy"][x.energy].append(x)
        info_list["speechiness"][x.speechiness].append(x)
        info_list["acousticness"][x.acousticness].append(x)
        info_list["instrumentalness"][x.instrumentalness].append(x)
        info_list["valence"][x.valence].append(x)
        info_list["liveness"][x.liveness].append(x)
        info_list["tempo"][x.tempo].append(x)
    return info_list

"""function that filters out and deletes smaller dictorinaries"""
def filterCategory(category_list,playlist_length):
    global categories
    for x in categories:
        try:
            for y in category_list[x]:
                if len(category_list[x][y])/playlist_length <= 0.15:
                    del category_list[x]
        except KeyError:
            pass
    return category_list

"""function that removes duplicate entries from the bigger playlist"""
def removingDuplicates(category_list):
    for catA in category_list:
        for catB in category_list:
            if catA == catB:
                continue
            for ranA in category_list[catA]:
                for ranB in category_list[catB]:
                    for track in category_list[catA][ranA]:
                        if track in category_list[catB][ranB]:
                            if len(category_list[catB][ranB]) > len(category_list[catA][ranA]):
                                category_list[catB][ranB].remove(track)
                            else:
                                category_list[catA][ranA].remove(track)

    return category_list

"""Function to convert object song to json"""
def objToDict(song):
    return song.__dict__

"""Function to convert a json formated data back to obj song type"""
def jsonToObj(json):
    return song(json["id"],json["danceability"],json["energy"],json["speechiness"],json["acousticness"],json["instrumentalness"],json["valence"],json["liveness"],json["tempo"],json["name"],json["artist"],json["image"])

"""Function used to create playlist on Spotify for users"""
def createPlaylist(genre,type,songs,request):
    sp = authcode("playlist-modify-public",request)
    user = sp.me()
    playlist = sp.user_playlist_create(user['id'], name=(type.capitalize()+" "+genre.capitalize()), public=True, collaborative=False, description='Sliced Playlist')
    ids = [song.id for song in songs]
    sp.user_playlist_add_tracks(user['id'],playlist['uri'],ids)
