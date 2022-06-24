from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from SP.helper import *
import json
# Create your views here.

@csrf_exempt
def homepage(request):
    if request.method == "GET":
        return render(request,'homepage.html')

@csrf_exempt
def playlist(request):
    global tracklist
    playlistId = request.POST.get('playlistId')
    authentication = authcode()
    tracklist = playlistItems(authentication,playlistId)
    jsonTrack = json.dumps(tracklist, default=objToDict)
    request.session["tracklist"] = jsonTrack
    return render(request,'playlist.html',{ 'playlist' : tracklist })

def analysis(request):
    tracklist = request.session["tracklist"]
    tracklist = json.loads(tracklist)
    tracklist = [jsonToObj(entry) for entry in tracklist]
    sepratedPlaylist = sepration(tracklist)
    sepratedPlaylist = filterCategory(sepratedPlaylist,len(tracklist))
    sepratedPlaylist = removingDuplicates(sepratedPlaylist)
    return render(request,'analysis.html',{ 'playlists' : sepratedPlaylist})
