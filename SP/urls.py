from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.homepage, name='home'),
    path('home/playlist/',views.playlist),
    path('analysis/',views.analysis, name='analysis'),
]
