from django.shortcuts import render
from django.http import HttpResponse
import logging
from setlist_api_functions import get_artist_by_name
from setlist_api_functions import get_artist_info
from setlist_api_functions import concerts_with_encored_songs
from setlist_api_functions import popular_encored_songs
from setlist_api_functions import youtube_song
import requests
import json

# Get an instance of a logger
logger = logging.getLogger("GigM8")

def index(request):
    logger.debug("*********Into index View*******")
    return render(request, 'index.html')


def events(request):
    return render(request, 'events.html')


def history(request, artist_name):
    artist = artist_name.replace('_', ' ')
    artist_id = get_artist_by_name(artist)
    # Get info about the artist
    info = get_artist_info(artist_id)
    # Get 10 most played songs

    # Get albums of the songs

    # Get percentage of events with encored songs
    e_p = concerts_with_encored_songs(artist_id)*100
    # Get popular encored songs
    p_e = popular_encored_songs(artist_id)
    for s in p_e:
        s['y'] = youtube_song(s['name'], artist_name)
    data = {'artistInfo': info, 'mostPlayed': [], 'encorePercentage': e_p, 'popularEncored': p_e}
    return render(request, 'history.html', data)



#Size of the pages on each search of the API
PAGE_SIZE = 12
#Comma separated list of the desired sizes of the images
IMAGE_SIZES = "large"

#Script to get events by location search
def EventsbyLocation(request,page):

    location="Finland" #can be sent from frontend
    pageNumber = page
    payload = {'app_key': 'bdNbdBzr4dD6Ghr3', 'location': location ,"within": 20, "unit": "km",
               "category": "music", "sort_order": "popularity", "page_size": PAGE_SIZE,
               "page_number": pageNumber, "image_sizes": IMAGE_SIZES}
    r = requests.get('http://api.eventful.com/json/events/search', params=payload)
    Json = r.json()
    events = []
    for i in range(0, len(Json['events']['event'])):
        event = Json['events']['event'][i]
        events.append({'id': event['id'],'title': event['title'],'url': event['url'], 'description': event['description'],
                        'startTime': event['start_time'],'venueName': event['venue_name'], 'venueUrl': event['venue_url'],
                        'startTime': event['start_time'], 'cityName' : event['city_name'], 'regionName': event['region_name'],
                        'countryName': event['country_name'], 'image': event['image'], 'performers': event['performers']})
        i += 1
    data = {
            "pageCount": int(Json["page_count"]), "totalItems": int(Json["total_items"]), "events": events
        }
    return HttpResponse(json.dumps(data))