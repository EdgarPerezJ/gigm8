__author__ = 'Sufian'
import logging
import requests
from django.http import HttpResponse
from django.http import JsonResponse
import json

# Get an instance of a logger
logger = logging.getLogger("GigM8")
#Size of the pages on each search of the API
PAGE_SIZE = 12
#Comma separated list of the desired sizes of the images
IMAGE_SIZES = "large"
#Distance within the search will be done when using geolocation
WITHIN_DISTANCE = 20
#Unit of the distance
UNIT_DISTANCE = "km"

##Script to get events by location search
def getEventsbyLocation(request,page):

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
    return data

# gets the details of one specific event
def getEventDetails(request,id):
    eveid=id
    payload = {'app_key': 'bdNbdBzr4dD6Ghr3', 'id': eveid, "image_sizes": "large"}
    r = requests.get('http://api.eventful.com/json/events/get', params=payload)
    Json = r.json()
    data={
        'title':Json['title'],'description':Json['description'],'performer':Json['performers'],'venueName':Json['venue_name'],'date':Json['start_time'],'image':Json['images']
    }
    return data

#Get the events by the geolocation
def get_events_geolocation(coordinates, page_number):
    payload = {'app_key': 'bdNbdBzr4dD6Ghr3', 'location': coordinates, "within": WITHIN_DISTANCE, "unit": UNIT_DISTANCE,
               "category": "music", "sort_order": "popularity", "page_size": PAGE_SIZE,
               "page_number": page_number, "image_sizes": IMAGE_SIZES}
    r = requests.get('http://api.eventful.com/json/events/search', params=payload)
    json = r.json()
    events = []
    for i in range(0, len(json['events']['event'])):
        event = json['events']['event'][i]
        performers = []
        if(event['performers'] != None):
            if(isinstance(event['performers']['performer'], list)):
                for j in range(0, len(event['performers']['performer'])):
                    performers.append(event['performers']['performer'][j])
                    j += 1
            else:
                performers.append(event['performers']['performer'])
        else:
            performers.append(event['performers'])
        events.append({'id': event['id'],'title': event['title'],'url': event['url'], 'description': event['description'],
                        'startTime': event['start_time'],'venueName': event['venue_name'], 'venueUrl': event['venue_url'],
                        'startTime': event['start_time'], 'cityName' : event['city_name'], 'regionName': event['region_name'],
                        'countryName': event['country_name'], 'image': event['image'], 'performers': performers})
        i += 1
    return {"pageCount": int(json["page_count"]), "totalItems": int(json["total_items"]), "events": events}

#Get the events by artist
def get_artists(page, artistName):
    #First the artist need to be searched.
    paramsArtist = { 'app_key': 'bdNbdBzr4dD6Ghr3', "keywords": artistName}
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
    return {"performer": performer, "pageCount": int(jsonEvents["page_count"]), "totalItems": int(jsonEvents["event_count"]), "events": events}
