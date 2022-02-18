import requests
import json
from bs4 import BeautifulSoup


# Convert abbreviated number to integer
def string_to_integer(string):
    characters = ['+', 'K', 'M', 'B']
    clean_string = string
    for character in characters:
        clean_string = clean_string.replace(character, '')
    number = float(clean_string)
    if 'K' in string:
        number *= 10**3
    elif 'M' in string:
        number *= 10**6
    elif 'B' in string:
        number *= 10**9
    return int(number)


# Artist ID from the ?artistId=
artist_id = input('Type in the artist id: ')

# MelOn Headers
melon_headers = {
    'Referer':
    'https://www.melon.com/artist/timeline.htm?artistId=' + artist_id,
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# Paging URL API
paging_url = 'https://www.melon.com/artist/songPaging.htm'
paging_query = {
    'startIndex': '1',
    'pageSize': '2000',
    'orderBy': 'ISSUE_DATE',
    'artistId': artist_id
}

paging_songs = requests.get(paging_url,
                            params=paging_query,
                            headers=melon_headers).text
paging_songs_response = BeautifulSoup(paging_songs, 'html.parser')
song_ids = []
for tr in paging_songs_response.select('div.tb_list table tbody tr'):
    song_id = tr.select('button.btn_icon.like')[0].attrs['data-song-no']
    song_ids.append(song_id)

# Variables set to zero to add them as the loop goes
total_streams = 0
total_listeners = 0

# Sum every song streams and listeners
n = 0
for song_id in song_ids:
    n += 1
    print(f'Analizing data from song {n}-{len(song_ids)}')
    api_request = requests.get(
        f'https://m2.melon.com/m6/chart/streaming/card.json?cpId=AS40&cpKey=14LNC3&appVer=6.0.0&songId={song_id}',
        headers=melon_headers).text
    api_response = json.loads(api_request)['response']
    if api_response['VIEWTYPE'] == "2":
        if api_response['STREAMUSER'] != '':
            total_listeners += string_to_integer(
                api_response['STREAMUSER'])
        if api_response['STREAMCOUNT'] != '':
            total_streams += string_to_integer(
                api_response['STREAMCOUNT'])

# Print the results
print(total_listeners)
print(total_streams)
