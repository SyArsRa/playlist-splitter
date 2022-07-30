from django.shortcuts import render, redirect , reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib import messages
from SP.helper import *
import json
import logging
# Create your views here.

@csrf_exempt
def homepage(request):
    list(messages.get_messages(request))
    if request.method == "GET":
        request.session["tracklist"] = []
        return render(request,'homepage.html')

def homepageError(request):
    if request.method == "GET":
        request.session["tracklist"] = []
        return render(request,'homepage.html')

@csrf_exempt
def playlist(request):
    global tracklist
    playlistId = request.POST.get('playlistId')
    #catching any exceptions that might occur when sending requests to Spotify API
    try:
        tracklist = playlistItems(playlistId,request)
    except Exception:
        logging.exception("message")
        messages.error(request,'Incorrect Playlist link')
        return redirect('/Error/')
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
            logging.exception("message")
            messages.error(request,'Unexpected Error, Please try again later')
            return redirect('/Error/')
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
            logging.exception("message")
            messages.error(request,'Unexpected Error, Please try again later')
            return redirect('/Error/')
        genre, type  = request.POST.get("btnPlaylist").split()
        if genre+type not in request.session['created']:
            request.session["created"] += [genre+type]
            #catching any exceptions that might occur when sending requests to Spotify API
            try:
                createPlaylist(genre,type,sepratedPlaylist[genre][type],request)
            except Exception:
                logging.exception("message")
                messages.error(request,'Unexpected Error, Please try again later')
                return redirect('/Error/')
        return render(request,'analysis.html', { 'playlists' : sepratedPlaylist, 'created' : request.session['created']})
