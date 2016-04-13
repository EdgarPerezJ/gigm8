__author__ = 'Sufian'
import logging
import requests
from django.http import HttpResponse
from django.http import JsonResponse

# Get an instance of a logger
logger = logging.getLogger("GigM8")
#Size of the pages on each search of the API
PAGE_SIZE = 10
#Comma separated list of the desired sizes of the images
IMAGE_SIZES = "medium"

#Script to get events by location search
def EventsbyLocation(request):
    location="Finland" #can be sent from frontend
    pageNumber = 1
    payload = {'app_key': 'bdNbdBzr4dD6Ghr3', 'location': location ,"within": 20, "unit": "km",
               "category": "music", "sort_order": "popularity", "page_size": PAGE_SIZE,
               "page_number": pageNumber, "image_sizes": IMAGE_SIZES}
    r = requests.get('http://api.eventful.com/json/events/search', params=payload)
    json = r.json()
    events = []
    for i in range(0, len(json['events']['event'])):
        event = json['events']['event'][i]
        events.append({'id': event['id'],'title': event['title'],'url': event['url'], 'description': event['description'],
                        'startTime': event['start_time'],'venueName': event['venue_name'], 'venueUrl': event['venue_url'],
                        'startTime': event['start_time'], 'cityName' : event['city_name'], 'regionName': event['region_name'],
                        'countryName': event['country_name'], 'image': event['image'], 'performers': event['performers']})
        i += 1
    return JsonResponse({"pageCount": int(json["page_count"]), "totalItems": int(json["total_items"]), "events": events})

# gets the details of one specific event
def EventDetails(request):
    id="E0-001-087782406-3" #can be sent from frontend
    payload = {'app_key': 'bdNbdBzr4dD6Ghr3', 'id': id,"image_sizes": "large"}
    r = requests.get('http://api.eventful.com/json/events/get', params=payload)
    json = r.json()
    results=[]
    results.append({'title':json['title'],'description':json['description']})
    return JsonResponse(json)

#Get the events by the geolocation
def eventsByGeolocation(request):
    coordinates = "50.9377596,-1.376547"
    pageNumber = 1
    payload = {'app_key': 'bdNbdBzr4dD6Ghr3', 'location': coordinates, "within": 20, "unit": "km",
               "category": "music", "sort_order": "popularity", "page_size": PAGE_SIZE,
               "page_number": pageNumber, "image_sizes": IMAGE_SIZES}
    r = requests.get('http://api.eventful.com/json/events/search', params=payload)
    json = r.json()
    events = []
    for i in range(0, len(json['events']['event'])):
        event = json['events']['event'][i]
        events.append({'id': event['id'],'title': event['title'],'url': event['url'], 'description': event['description'],
                        'startTime': event['start_time'],'venueName': event['venue_name'], 'venueUrl': event['venue_url'],
                        'startTime': event['start_time'], 'cityName' : event['city_name'], 'regionName': event['region_name'],
                        'countryName': event['country_name'], 'image': event['image'], 'performers': event['performers']})
        i += 1
    return JsonResponse({"pageCount": int(json["page_count"]), "totalItems": int(json["total_items"]), "events": events})

#Get the events by artist
def eventsByArtist(request):
    artistName = "The Horrors" #This will be a parameter from
    #First the artist need to be searched.
    paramsArtist = { 'app_key': 'bdNbdBzr4dD6Ghr3', "keywords": artistName }
    r = requests.get('http://api.eventful.com/json/performers/search', params=paramsArtist)
    json = r.json()
    performer = json['performers']['performer'][0]
    performerId = performer['id']

    #Then the events of that artist using it's ID should be retrieved.
    pageNumber = 1
    paramEvents = {'app_key': 'bdNbdBzr4dD6Ghr3', "id": performerId,"page_size": PAGE_SIZE,
               "page_number": pageNumber}
    rEvents = requests.get('http://api.eventful.com/json/performers/events/list', params=paramEvents)
    jsonEvents = rEvents.json()
    eventCount = int(jsonEvents['event_count'])
    events = []
    if eventCount == 1:
        events.append(jsonEvents['event'])
    else:
        for i in range(0, len(jsonEvents['event'])):
            events.append(jsonEvents['event'])
            i += 1
    #In this particular search we retrieve artists and also events from those artists.
    return JsonResponse({"performer": performer, "pageCount": int(jsonEvents["page_count"]), "totalItems": int(jsonEvents["event_count"]), "events": events})
