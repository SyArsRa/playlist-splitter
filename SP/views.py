from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib import messages
from SP.helper import *
from json import loads , dumps
from logging import exception
# Create your views here.


#Homepage
def homepage(request):
    list(messages.get_messages(request))
    request.session["tracklist"] = []
    return render(request,'homepage.html')

#Homepage For Errors
def homepageError(request):
    request.session["tracklist"] = []
    return render(request,'homepage.html')

#Spotify API Authorization
@csrf_exempt
def authorization(request):
    try:
        return redirect(authcode())
    except Exception:
        messages.error(request,'Unexpected Error, Please Try Again Later')
        return redirect('/Error/')

#Spotify API Callback
def reponse(request):
    try:
        authcode = request.GET.get('code')
        request.session["token"] = tokens(authcode)
        request.session["userId"] = me(request.session["token"])
    except Exception:
        messages.error(request,'Unexpected Error, Please Try Again Later')
        return redirect('/Error/')
    return redirect('/choice/')

#Displays Users Playlist
def choice(request):
    try:
        items = playlists(request.session["token"])
    except Exception:
        messages.error(request,'Unexpected Error, Please Try Again Later')
        return redirect('/Error/')
    return render(request,'choice.html',{ 'playlists': items })

#Displays Songs In The Playlist
@csrf_exempt
def playlist(request):
    global tracklist
    playlistId = request.POST.get('playlistId')
    #catching any exceptions that might occur when sending requests to Spotify API
    try:
        tracklist = playlistItems(playlistId,request.session["token"])
    except Exception:
        exception("message")
        messages.error(request,'Unexpected Error, Please Try Again Later')
        return redirect('/Error/')
    jsonTrack = dumps(tracklist, default=objToDict)
    request.session["tracklist"] = jsonTrack
    return render(request,'playlist.html',{ 'playlist' : tracklist })

#Displays Sliced Playlist
@csrf_exempt
def analysis(request):
    #when request method is get
    if request.method == 'GET':
        tracklist = request.session["tracklist"]
        tracklist = loads(tracklist)
        tracklist = [jsonToObj(entry) for entry in tracklist]
        #catching any exceptions that might occur
        try:
            sepratedPlaylist = sepration(tracklist)
        except Exception:
            exception("message")
            messages.error(request,'Unexpected Error, Please Try Again Later')
            return redirect('/Error/')
        request.session['playlistClusters'] = dumps(sepratedPlaylist, default=objToDict)
        request.session["created"] = []
        return render(request,'analysis.html',{ 'playlists' : sepratedPlaylist})
    #runs when request method is not get
    else:
        #catching any exceptions that might occur
        try:
            sepratedPlaylist = request.session['playlistClusters']
            sepratedPlaylist = loads(sepratedPlaylist)
            for entry in sepratedPlaylist:
                sepratedPlaylist[entry] = [ jsonToObj(song) for song in sepratedPlaylist[entry]]
        except Exception:
            exception("message")
            messages.error(request,'Unexpected Error, Please Try Again Later')
            return redirect('/Error/')
        cluster  = request.POST.get("btnPlaylist")
        if cluster not in request.session['created']:
            request.session["created"] += [cluster]
            #catching any exceptions that might occur when sending requests to Spotify API
            try:
                createPlaylist(cluster,sepratedPlaylist[cluster],request.session["token"],request.session["userId"])
            except Exception:
                exception("message")
                messages.error(request,'Unexpected Error, Please try again later')
                return redirect('/Error/')
        return render(request,'analysis.html', { 'playlists' : sepratedPlaylist, 'created' : request.session['created']})
