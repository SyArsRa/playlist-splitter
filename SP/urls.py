from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage, name='home'),
    path('Error/',views.homepageError, name='homepageError'),
    path('playlist/',views.playlist, name='playlist'),
    path('analysis/',views.analysis, name='analysis'),
]
