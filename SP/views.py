from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from SP.helper import *
# Create your views here.

@csrf_exempt
def homepage(request):
    if request.method == "GET":
        return render(request,'homepage.html')

@csrf_exempt
def analysis(request):
    playlistId = request.POST.get('playlistId')
    authentication = authcode()
    tracklist = playlistitems(authentication,playlistId)
    return render(request,'playlist.html',{ 'playlist' : tracklist })
