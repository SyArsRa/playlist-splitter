from django.shortcuts import render, redirect , reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib import messages
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
    #catching any exceptions that might occur when sending requests to Spotify API
    try:
        tracklist = playlistItems(playlistId)
    except Exception:
        messages.error(request,'Incorrect Playlist link')
        return redirect('')
    jsonTrack = json.dumps(tracklist, default=objToDict)
    request.session["tracklist"] = jsonTrack
    return render(request,'playlist.html',{ 'playlist' : tracklist })

@csrf_exempt
def analysis(request):
    #when request method is get
    if request.method == 'GET':
        tracklist = request.session["tracklist"]
        tracklist = json.loads(tracklist)
        tracklist = [jsonToObj(entry) for entry in tracklist]
        #catching any exceptions that might occur when sending requests to Spotify API
        try:
            sepratedPlaylist = sepration(tracklist)
            sepratedPlaylist = filterCategory(sepratedPlaylist,len(tracklist))
            sepratedPlaylist = removingDuplicates(sepratedPlaylist)
        except Exception:
            messages.error(request,'Unexpected Error, Please try again later')
            return redirect('')
        request.session["created"] = []
        return render(request,'analysis.html',{ 'playlists' : sepratedPlaylist})
    #runs when request method is not get
    else:
        tracklist = request.session["tracklist"]
        tracklist = json.loads(tracklist)
        tracklist = [jsonToObj(entry) for entry in tracklist]
        #catching any exceptions that might occur when sending requests to Spotify API
        try:
            sepratedPlaylist = sepration(tracklist)
            sepratedPlaylist = filterCategory(sepratedPlaylist,len(tracklist))
            sepratedPlaylist = removingDuplicates(sepratedPlaylist)
        except Exception:
            messages.error(request,'Unexpected Error, Please try again later')
            return redirect('')
        genre, type  = request.POST.get("btnPlaylist").split()
        if genre+type not in request.session['created']:
            request.session["created"] += [genre+type]
            #catching any exceptions that might occur when sending requests to Spotify API
            try:
                createPlaylist(genre,type,sepratedPlaylist[genre][type])
            except Exception:
                messages.error(request,'Unexpected Error, Please try again later')
                return redirect('')
        return render(request,'analysis.html', { 'playlists' : sepratedPlaylist, 'created' : request.session['created']})
