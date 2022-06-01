import sys
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth


"""Important Variable Declarations for api"""
os.environ["SPOTIPY_CLIENT_ID"] = 'ebbeb9d031a344878ac299f009ef5a27'
os.environ["SPOTIPY_CLIENT_SECRET"]='89be84be843e4627be7f5292846ecfd0'
os.environ["SPOTIPY_REDIRECT_URI"]='http://localhost:8888/callback'

"""temporary variables """
playlistURL = "https://open.spotify.com/playlist/1t6sBuZrFpwsF80UYv9bes?si=f9a41048bd754b47"

"""Global Variable Declarations"""
categories = ["danceability","energy","speechiness","acousticness","instrumentalness","valence","liveness"]

"""Class that stores every song in the playlist_items"""
class song:
    def __init__(self,id,danceability,energy,speechiness,acousticness,instrumentalness,valence,liveness,tempo):
        self.id = id
        self.danceability = danceability
        self.energy = energy
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.liveness = liveness
        self.tempo = tempo

"""function to get authentication from Spotfiy to usee their api"""
def authcode():
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp


"""extracts playlist from spotify api and then extracts their various characteristics
(important note - play_items method on gets first 100 songs from playlist) and return a list of object song with each
object storing a important informations about songs"""
def playlistitems(sp,playlistURL):
    global categories
    start = 0
    total = 1
    playlist = []
    while start < total:
        uri = []
        names = sp.playlist_items(playlistURL,offset=start)
        total = names["total"]
        for y in range(len(names["items"])):
            uri.append(names["items"][y]["track"]["uri"])
        features = sp.audio_features(uri)
        for track in features:
            data = ["high" if float(track[stat]) > 0.5 else "low" for stat in categories]
            if int(track["tempo"]) > 108:
                data += ["high"]
            else:
                data += ["low"]
            analyzed = song(track["uri"],data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
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

#    for i in categories:
#        print(i , len(info_list[i]["high"]),len(info_list[i]["low"]))
    return info_list

"""function that filters out and deletes smaller dictorinaries"""
def filter_category(category_list,playlist_length):
    global categories
    for x in categories:
        for y in category_list[x]:
            if len(category_list[x][y])/playlist_length <= 0.15:
                del category_list[x]
                break                
    return category_list

"""function that removes duplicate entries from the bigger playlist"""
def removing_duplicates(category_list):
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
    for i in categories:
        try:
            print(i , len(category_list[i]["high"]),len(category_list[i]["low"]))
        except KeyError:
            pass
    return category_list


sp = authcode()
tr = playlistitems(sp,playlistURL)
list = sepration(tr)
rr = filter_category(list,len(tr))
removing_duplicates(rr)
