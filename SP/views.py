from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SP.helper import *
import json
# Create your views here.

@csrf_exempt
def homepage(request):
    if request.method == "GET":
        request.session["tracklist"] = []
        return render(request,'homepage.html')

@csrf_exempt
def playlist(request):
    global tracklist
    playlistId = request.POST.get('playlistId')
    tracklist = playlistItems(playlistId)
    jsonTrack = json.dumps(tracklist, default=objToDict)
    request.session["tracklist"] = jsonTrack
    return render(request,'playlist.html',{ 'playlist' : tracklist })

@csrf_exempt
def analysis(request):
    if request.method == 'GET':
        tracklist = request.session["tracklist"]
        tracklist = json.loads(tracklist)
        tracklist = [jsonToObj(entry) for entry in tracklist]
        sepratedPlaylist = sepration(tracklist)
        sepratedPlaylist = filterCategory(sepratedPlaylist,len(tracklist))
        sepratedPlaylist = removingDuplicates(sepratedPlaylist)
        request.session["created"] = []
        return render(request,'analysis.html',{ 'playlists' : sepratedPlaylist})
    else:
        tracklist = request.session["tracklist"]
        tracklist = json.loads(tracklist)
        tracklist = [jsonToObj(entry) for entry in tracklist]
        sepratedPlaylist = sepration(tracklist)
        sepratedPlaylist = filterCategory(sepratedPlaylist,len(tracklist))
        sepratedPlaylist = removingDuplicates(sepratedPlaylist)
        genre, type  = request.POST.get("btnPlaylist").split()
        if genre+type not in request.session['created']:
            request.session["created"] += [genre+type]
            createPlaylist(genre,type,sepratedPlaylist[genre][type])
        return render(request,'analysis.html', { 'playlists' : sepratedPlaylist, 'created' : request.session['created']})
