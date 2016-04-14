# coding=utf-8
import requests
import json
import logging
import urllib
import urllib2
import unicodedata
from bs4 import BeautifulSoup
import time
from countryList import country_list

"""
Function that finds index of a dictionary in a list that contains the key with a certain value
"""

# Get an instance of a logger
logger = logging.getLogger("GigM8")

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


"""
This function returns a URL to the lyrics
Input:
    - artist: Artist name
    - song: Song name
Output:
    - URL to lyrics n music
"""


def lyrics(artist, song):
    url = 'http://api.lyricsnmusic.com/songs?api_key=aaef0ce9b42a333034967bfcbb1349&artist=' + artist + '&track=' + song
    r = requests.get(url)
    d = json.loads(r.text)
    return d[0]['url']


"""
This function returns a youtube video for a song by a group
Input:
    - song: name of a song
    - art: name of song´s artist
Output:
    - Youtube URL
"""


def youtube_song(song, art):
    text_to_search = song + ' ' + art
    text_to_search = unicodedata.normalize('NFKD', text_to_search).encode('ascii', 'ignore')
    query = urllib.quote(text_to_search)
    url = "https://www.youtube.com/results?search_query=" + query
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0')
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    song_link = ''
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        song_link = 'https://www.youtube.com' + vid['href']
        break
    return song_link


"""
This function returns a youtube video for a song by a group WITH LYRICS
Input:
    - song: name of a song
    - art: name of song´s artist
Output:
    - Youtube URL
"""


def youtube_song_lyrics(song, art):
    text_to_search = song + ' ' + art + ' lyrics'
    text_to_search = unicodedata.normalize('NFKD', text_to_search).encode('ascii', 'ignore')
    query = urllib.quote(text_to_search)
    url = "https://www.youtube.com/results?search_query=" + query
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0')
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    song_link = ''
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        song_link = 'https://www.youtube.com' + vid['href']
        break
    return song_link


"""
Returns a list of the last 10 events´ venues info (only for the events that already have a setlist):
{
  "@id": "43d62307",
  "@name": "Palacio de la Ópera",
  "city": {
    "@id": "3119841",
    "@name": "Corunna",
    "@state": "Galicia",
    "@stateCode": "58",
    "coords": {
      "@lat": "43.371349638664",
      "@long": "-8.39600086212158"
    },
    "country": {
      "@code": "ES",
      "@name": "Spain"
    }
}
Input:
    - mbid: musicbrainz id of an artist
Output:
    - A list of dictionaries
"""


def last_events_venues(mbid):
    url = 'http://api.setlist.fm/rest/0.1/artist/' + mbid + '/setlists.json?p=1'
    r = requests.get(url)
    d = json.loads(r.text)
    event_count = 10
    event_list = []
    setlists_list = d['setlists']['setlist']
    for l in setlists_list:
        if l['sets'] != "":
            event_count -= 1
            if event_count == -1:
                break
            event = l['venue']
            event_list.append(event)
    return event_list


"""
This function returns the most played encored songs
by a group in their the last 20 concerts (sorted by frequency)
Input:
    - armbid = artist musicbrainz id
Output:
    - A list of dictionaries  [{'count': 1, 'name': 'song title'},...]
    - If there are no encore songs then: -1
"""


def popular_encored_songs(armbid):
    url = 'http://api.setlist.fm/rest/0.1/artist/' + armbid + '/setlists.json?p=1'
    r = requests.get(url)
    d = json.loads(r.text)
    if any('error' in e for e in d):
        error = True
        while error:
            r = requests.get(url)
            d = json.loads(r.text)
            if not any('error' in e for e in d):
                error = False
    setlists_list = d['setlists']['setlist']
    total_list = []
    encore_present = False
    for l in setlists_list:
        if l['sets'] != "":
            set_type = type(l['sets']['set'])
            if set_type is list:
                full_list = l['sets']['set']
                if any('@encore' in d for d in full_list):  # Find out if there are any encored lists
                    encore_present = True
                    encore_list = []
                    for x in full_list:
                        if '@encore' in x:
                            if type(x['song']) is list:
                                for ll in x['song']:
                                    encore_list.append(ll)
                            else:
                                encore_list.append(x['song'])
                    for el in encore_list:
                        el_name = el['@name']
                        if any(d['name'] == el_name for d in total_list):
                            song_index = find(total_list, 'name', el_name)
                            total_list[song_index]['count'] += 1
                        else:
                            total_list.append({'name': el_name, 'count': 1})
    if encore_present:
        total_list.sort(key=lambda x: x['count'])
        total_list.reverse()
        return total_list
    else:
        return -1


"""
This function returns a percentage of the concerts in which an artist
played songs requested by the audience. (For last 20 concerts)
Input:
    - armbid = artist musicbrainz id
Output:
    - A percentage of the concerts with encored songs
"""


def concerts_with_encored_songs(armbid):
    url = 'http://api.setlist.fm/rest/0.1/artist/' + armbid + '/setlists.json?p=1'
    r = requests.get(url)
    d = json.loads(r.text)
    if any('error' in e for e in d):
        error = True
        while error:
            r = requests.get(url)
            d = json.loads(r.text)
            if not any('error' in e for e in d):
                error = False
    setlist_count = 20
    setlists_list = d['setlists']['setlist']
    encore_concert_count = 0
    for l in setlists_list:
        if l['sets'] != "":
            set_type = type(l['sets']['set'])
            if set_type is list:
                full_list = l['sets']['set']
                if any('@encore' in d for d in full_list):  # Find out if there are any encored lists
                    encore_concert_count += 1
    percentage = 0
    if encore_concert_count != 0:
        percentage = encore_concert_count / float(setlist_count)
    return percentage


"""
This function returns the album name to which a song belongs
Input:
    - mbid = musicbrainz artist id
    - sn = song name
Output:
    - Name of the album to which the song belongs to (and release date) {'album': 'album title', 'date': 'release date'}
"""


def album_of_song(mbid, sn):
    url = "http://musicbrainz.org/ws/2/recording?query=" + sn + " AND arid:" + mbid + "&fmt=json"
    r = requests.get(url)
    d = json.loads(r.text)
    if any('error' in e for e in d):
        error = True
        while error:
            r = requests.get(url)
            d = json.loads(r.text)
            if not any('error' in e for e in d):
                error = False
    date = time.strptime('9999-12-31', "%Y-%m-%d")
    final = {'album': '', 'date': date}
    for rec in d['recordings']:
        if any('releases' in r for r in rec):
            for rel in rec['releases']:
                if any('date' in x for x in rel):
                    if any('status' in g for g in rel):
                        if rel['status'] == 'Official':
                            if not any('secondary-types' in s for s in rel['release-group']):
                                if len(rel['date']) == 4:
                                    new_date = time.strptime(str(rel['date']), "%Y")
                                elif len(rel['date']) == 7:
                                    new_date = time.strptime(str(rel['date']), "%Y-%m")
                                else:
                                    new_date = time.strptime(str(rel['date']), "%Y-%m-%d")
                                if new_date < final['date']:
                                    final['date'] = new_date
                                    final['album'] = rel['title']
    return final


"""
This function returns the albums to which input songs are related to
Input:
    - armbid = musicbrainz artist id
    - sl = list of song names
Output:
    - [{'album': 'album name', 'songList': [song1, song2,...]},'percentage':''},...]
"""


def albums_of_songs(armbid, sl):
    final_list = []
    sl_size = len(sl)
    for s in sl:
        album = album_of_song(armbid, s)['album']
        if album == '':
            album = 'Other'
        if len(final_list) == 0:
            aux = {'album': album, 'songList': [s], 'percentage': 0}
            final_list.append(aux)
        else:
            album_index = find(final_list, 'album', album)
            if album_index == -1:
                aux = {'album': album, 'songList': [s], 'percentage': 0}
                final_list.append(aux)
            else:
                final_list[album_index]['songList'].append(s)
        for f in final_list:
            f_l_size = len(f['songList'])
            f['percentage'] = round(f_l_size / float(sl_size), 2)*100
    final_list = sorted(final_list, key=lambda k: k['percentage'])
    final_list = final_list[::-1]
    return final_list


"""
Function that returns the musicbrainz id for a given name of an artist
"""


def get_artist_by_name(name):
    url = 'http://musicbrainz.org/ws/2/artist/?query=artist:' + name + '&fmt=json'
    r = requests.get(url)
    d = json.loads(r.text)
    if any('error' in e for e in d):
        error = True
        while error:
            r = requests.get(url)
            d = json.loads(r.text)
            if not any('error' in e for e in d):
                error = False
    artists_list = d['artists']
    return artists_list[0]['id']


"""
Function that returns musicbrainz info for a determined id
 - Input: musicbrainz artist id
 - Output: id, name, type, life-span, country and disambiguation
"""


def get_artist_info(mbid):
    url = 'http://musicbrainz.org/ws/2/artist/' + mbid + '?fmt=json'
    r = requests.get(url)
    d = json.loads(r.text)
    if any('error' in e for e in d):
        error = True
        while error:
            r = requests.get(url)
            d = json.loads(r.text)
            if not any('error' in e for e in d):
                error = False
    name = d['name']
    kind = d['type']
    gender = ''
    if kind == 'Person':
        gender = d['gender']
    country = False
    if d['country'] is not None:
        country_code = d['country']
        c_index = find(country_list, 'code', country_code)
        country = country_list[c_index]['name']
    life_span = False
    if any('life-span' in x for x in d):
        if d['life-span']['begin'] is not None:
            life_span = {'s': d['life-span']['begin'][:4], 'e': d['life-span']['end']}
    disambiguation = False
    if any('disambiguation' in x for x in d):
        disambiguation = d['disambiguation']
    artist_info = {'id': mbid, 'n': name, 'type': kind, 'c': country, 'life': life_span, 'd': disambiguation, 'g': gender}
    return artist_info


"""
Get a list of artists from musicbrainz matching by a given name
Input:
    Artist name
Output:
    - country, disambiguation, type and ID
"""


def getArtistsByName(artistName):
    params = {'query': 'artist:' + artistName, 'fmt': 'json'}
    r = requests.get('http://musicbrainz.org/ws/2/artist/', params=params)
    jsonText = r.json()
    d = json.loads(r.text)
    artists_list = d['artists']
    outputInfo = ""
    for artist in artists_list:
        name = artist['name'] if any('name' in d for d in artist) else "No Info"
        country = artist['country'] if any('country' in d for d in artist) else "No Info"
        disambiguation = artist['disambiguation'] if any('disambiguation' in d for d in artist) else "No Info"
        gender = artist['gender'] if any('gender' in d for d in artist) else "No Info"
        artistType = artist['type'] if any('type' in d for d in artist) else "No Info"
        id = artist['id'] if any('id' in d for d in artist) else "No Info"
        outputInfo = outputInfo + name + "," + country + "," + disambiguation + "," + gender + "," + artistType + "," + id + "\n"
    logging.debug(outputInfo)


"""
Get a list of 10 most played songs ordered by frequency
Input:
    artist musicbrainz id
Output:
    - a dict of songs
"""


def get_most_played_songs_by_artist(mbid):
    url2 = 'http://api.setlist.fm/rest/0.1/artist/' + mbid + '/setlists.json?p=1'
    r2 = requests.get(url2)
    d2 = json.loads(r2.text)
    outputInfo = ""
    setlists_list = d2['setlists']['setlist']
    songs_list = []
    for l in setlists_list:
        if l['sets'] != "":
            set_type = type(l['sets']['set'])
            if set_type is list:
                for x in l['sets']['set']:
                    for ll in x['song']:
                        songs_list.append(ll)
    dict2 = {}
    for i in range(len(songs_list)):
        if type(songs_list[i]) is dict:
            if any(songs_list[i]['@name'] in d for d in dict2):
                dict2[songs_list[i]['@name']] = dict2[songs_list[i]['@name']] + 1
            else:
                dict2[songs_list[i]['@name']] = 1
            outputInfo = outputInfo + songs_list[i]['@name'] + "\n"

    dict2 = sorted(dict2.items(), key=lambda x: x[1])
    dict2.reverse()
    return dict2
