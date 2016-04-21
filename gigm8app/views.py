from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import logging
import unicodedata
from setlist_api_functions import get_artist_by_name, albums_of_songs, last_events_venues
from setlist_api_functions import get_artist_info
from setlist_api_functions import concerts_with_encored_songs
from setlist_api_functions import popular_encored_songs
from setlist_api_functions import youtube_song
from setlist_api_functions import get_setlist
from setlist_api_functions import get_setlist_encore
from setlist_api_functions import get_most_played_songs_by_artist
from eventful_api import getEventDetails
from eventful_api import getEventsbyLocation
import json
import eventful_api

# Get an instance of a logger
logger = logging.getLogger("GigM8")

def index(request):
    logger.debug("*********Into index View*******")
    return render(request, 'index.html')

def events(request):
    return render(request, 'events.html')

def details(request):
    return render(request, 'details.html')

def about(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'index.html')

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
    a_s = albums_of_songs(artist_id, m_p)
    # Get percentage of events with encored songs
    e_p = concerts_with_encored_songs(artist_id)*100
    # Get popular encored songs
    p_e = popular_encored_songs(artist_id)
    if p_e == -1:
        p_e = False
    else:
        for s in p_e:
            s['y'] = youtube_song(s['name'], artist_name)
    data = {'artistInfo': info, 'mostPlayed': m_p_d, 'albums': a_s, 'encorePercentage': e_p, 'popularEncored': p_e}
    return render(request, 'history.html', data)


def last_events(request, armbid):
    data = last_events_venues(armbid)
    return HttpResponse(json.dumps(data), content_type="application/json")


#Script to get events by location search
def EventsbyLocation(request,page):
    location = request.POST["location"]
    data=getEventsbyLocation(request,page,location)
    logger.debug("location: " + location)
    return HttpResponse(json.dumps(data))



# gets the details of one specific event
def EventDetails(request,id):
    data=getEventDetails(request,id)
    return HttpResponse(json.dumps(data))

#gets the events by geolocation
def events_by_geolocation(request, latitude, longitude, page):
    geolocation = latitude +","+longitude
    info = eventful_api.get_events_geolocation(geolocation, page)
    return JsonResponse(info)

#gets the artists by name
def artist_by_name(request, page):
    artistName = request.POST["artistName"]
    info = eventful_api.get_artists(page, artistName)
    return JsonResponse(info)

#gets the infor of an artist
def artist_by_id(request, id):
    info = eventful_api.get_artist_by_id(id)
    return render(request, 'profile.html', info)
    #return JsonResponse(info)

def setlist(request, artist_name, setlistid):
    # Get setlist
    raw_set_list = get_setlist(setlistid)
    setlist = []
    for s in raw_set_list:
        sf = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
        setlist.append(sf)
    setlist_d = []
    for s in setlist:
        setlist_d.append({'n': s, 'y': youtube_song(s, artist_name)})

    raw_set_list_encore = get_setlist_encore(setlistid)
    setlist_encore = []
    for s in raw_set_list_encore:
        sf = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
        setlist_encore.append(sf)
    setlist_d_encore = []
    for s in setlist_encore:
        setlist_d_encore.append({'n': s, 'y': youtube_song(s, artist_name)})
    data = {'setlist': setlist_d, 'setlist_encore': setlist_d_encore}
    return render(request, 'setlist.html', data)