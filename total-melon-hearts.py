import requests
import json
from bs4 import BeautifulSoup
from termcolor import colored

# Artist ID from the ?artistId=
artist_id = input('Type in the artist id: ')


# Global
def most_frequent(list):
    counter = 0
    num = list[0]
    for i in list:
        curr_frequency = list.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


artist_list = []
song_list = []

n = 1

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

# Hearts URL API
song_url = 'https://www.melon.com/commonlike/getSongLike.json'

# Stars URL API
stars_url = 'https://www.melon.com/artist/getArtistFanNTemper.json?artistId=' + artist_id

paging_songs = requests.get(paging_url,
                            params=paging_query,
                            headers=melon_headers).text
paging_response = BeautifulSoup(paging_songs, 'html.parser')
for tr in paging_response.select('div.tb_list table tbody tr'):
    for a in tr.select('td.t_left div.wrap.wrapArtistName #artistName a'):
        artist_feat = a.text
        artist_list.append(artist_feat)
    song_id = tr.select('button.btn_icon.like')[0].attrs['data-song-no']
    song_list.append(song_id)
artist_name = colored(most_frequent(artist_list), attrs=['bold'])
print(f'Collecting the songs by {artist_name}')
print(f'{len(song_list)} songs found on their profile')

artist_stars_api = requests.get(stars_url, headers=melon_headers).text
artist_stars_json = json.loads(artist_stars_api)
total_stars = artist_stars_json['fanInfo']['SUMMCNT']

total_hearts = 0
for song_ids in chunks(song_list, 100):
    x = len(song_ids)
    print(f'Analizing data from song {n}-{n+x-1}')
    n += x
    song_id_params = {'contsIds': song_ids}
    hearts_song = requests.get(song_url,
                               params=song_id_params,
                               headers=melon_headers).text
    hearts_song_json = json.loads(hearts_song)
    for h in hearts_song_json['contsLike']:
        hearts = h['SUMMCNT']
        total_hearts += hearts

print(
    f'{artist_name} has {total_hearts:,} {colored("hearts", "red")} and {total_stars:,} {colored("stars", "yellow")} on {colored("MelOn", "green")}'
)
