import requests
import json
from bs4 import BeautifulSoup
from termcolor import colored

# Artist ID from the ?artistId=
artistId = input('Type in the artist id: ')

# Global
def most_frequent(list): 
	counter = 0
	num = list[0] 
	for i in list: 
		curr_frequency = list.count(i) 
		if(curr_frequency > counter): 
			counter = curr_frequency 
			num = i 
	return num 

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

artistList = []
songList = []
heartsList = []

n = 1

# MelOn Headers
melonheaders = {
    'Referer': 'https://www.melon.com/artist/timeline.htm?artistId=' + artistId,
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# Paging URL API
pagsongUrl = 'https://www.melon.com/artist/songPaging.htm'
pagingQuerys = {
    'startIndex' : '1',
    'pageSize' : '2000',
    'orderBy' : 'ISSUE_DATE',
    'artistId' : artistId
}

# Hearts URL API
songUrl = 'https://www.melon.com/commonlike/getSongLike.json'

# Stars URL API
starsUrl = 'https://www.melon.com/artist/getArtistFanNTemper.json?artistId=' + artistId

pagingSongs = requests.get(pagsongUrl, params = pagingQuerys, headers = melonheaders).text
pagingResp = BeautifulSoup(pagingSongs, 'html.parser')
for tr in pagingResp.select('div.tb_list table tbody tr'):
    for a in tr.select('td.t_left div.wrap.wrapArtistName #artistName a'):
        artistFeat = a.text
        artistList.append(artistFeat)
    songId = tr.select('button.btn_icon.like')[0].attrs['data-song-no']
    songList.append(songId)
artistName = colored(most_frequent(artistList), attrs=['bold'])
print('Collecting the songs by', artistName)
print(len(songList), 'songs found on their profile')

artistStars = requests.get(starsUrl, headers = melonheaders).text
jsonStars = json.loads(artistStars)
starsTotal = jsonStars['fanInfo']['SUMMCNT']

for songIds in chunks(songList, 100):
    x = len(songIds)
    print(f'Analizing data from song {n}-{n+x-1}')
    n += x
    songIdparams = {
        'contsIds' : songIds
    }
    songHearts = requests.get(songUrl, params = songIdparams, headers = melonheaders).text
    jsonHearts = json.loads(songHearts)
    for h in jsonHearts['contsLike']:
        hearts = h['SUMMCNT']
        if hearts > 0:
            heartsList.append(hearts)
heartsTotal = sum(heartsList)

print(artistName, 'has', f'{heartsTotal:,}', colored('hearts', 'red'), 'and', f'{starsTotal:,}', colored('stars', 'yellow'), 'on', colored('MelOn', 'green'))