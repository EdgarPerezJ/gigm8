from django.shortcuts import render
from django.http import HttpResponse
import logging
import unicodedata
from setlist_api_functions import get_artist_by_name
from setlist_api_functions import get_artist_info
from setlist_api_functions import concerts_with_encored_songs
from setlist_api_functions import popular_encored_songs
from setlist_api_functions import youtube_song
from setlist_api_functions import albums_of_songs
from setlist_api_functions import get_most_played_songs_by_artist
from eventful_api import getEventDetails
from eventful_api import getEventsbyLocation
import requests
import json

# Get an instance of a logger
logger = logging.getLogger("GigM8")

def index(request):
    logger.debug("*********Into index View*******")
    return render(request, 'index.html')


def events(request):
    return render(request, 'events.html')

def details(request):
    return render(request, 'details.html')


def history(request, artist_name):
    artist = artist_name.replace('_', ' ')
    artist_id = get_artist_by_name(artist)
    # Get info about the artist
    info = get_artist_info(artist_id)
    # Get 10 most played songs
    raw_most_played = get_most_played_songs_by_artist(artist_id)
    raw_most_played_10 = raw_most_played[:10]
    m_p = []
    for s in raw_most_played_10:
        sf = unicodedata.normalize('NFKD', s[0]).encode('ascii', 'ignore')
        m_p.append(sf)
    m_p_d = []
    for s in m_p:
        m_p_d.append({'n': s, 'y': youtube_song(s, artist_name)})
    # Get albums of the songs
    # a_s = albums_of_songs(artist_id, m_p)
    # Get percentage of events with encored songs
    e_p = concerts_with_encored_songs(artist_id)*100
    # Get popular encored songs
    p_e = popular_encored_songs(artist_id)
    for s in p_e:
        s['y'] = youtube_song(s['name'], artist_name)
    data = {'artistInfo': info, 'mostPlayed': m_p_d, 'albums': [], 'encorePercentage': e_p, 'popularEncored': p_e}
    return render(request, 'history.html', data)



#Size of the pages on each search of the API
PAGE_SIZE = 12
#Comma separated list of the desired sizes of the images
IMAGE_SIZES = "large"

#Script to get events by location search
def EventsbyLocation(request,page):
    data=getEventsbyLocation(request,page)
    return HttpResponse(json.dumps(data))



# gets the details of one specific event
def EventDetails(request,id):
    data=getEventDetails(request,id)
    return HttpResponse(json.dumps(data))