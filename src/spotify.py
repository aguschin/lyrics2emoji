import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from spotify_constant import SPOTIFY_CONSTANT as sc

def get_songname_artist_from_result(result):
    return {
        sc.URI : result['track']['uri'], 
        sc.ARTIST : result['track']['artists'][0]['name'],
        sc.SONGNAME : result['track']['name']
    }

def get_top_song_from_playlist(
    playlist_URI : str, 
    limit : int = sc.TOP_SONG_LIMIT_CONSTANT, 
    market : str = sc.MARKET_CONSTANT
) -> list:
    '''
    get top N songs from the playlist

    args:
        playlist_URI : URI of spotify playlist
        limit : top song limit search
        market : region market song search
    return:
        list of songname, artist and URI as json
    '''
    results = sc.SPOTIFY.playlist_tracks(playlist_URI, limit=limit, market=market)

    list_of_song = []
    for song in results['items']:
        list_of_song.append(get_songname_artist_from_result(song))
    
    return list_of_song

def generate_genius_url(song_information : dict) -> str:
    '''
    generate lyric's url

    args:
        song_information : dict of songname, artist and URI
    return:
        genius_url : lyric's url
    '''
    artist = song_information[sc.ARTIST].replace(' ', '-')

    songname = song_information[sc.SONGNAME]
    songname = re.sub(re.compile('\(.*?\)|\[.*?\]|\{.*?\}'), '', songname).strip()
    songname = songname.replace('\'', '').replace('"', '').replace('’', '')
    songname = songname.replace('&', 'and') # special case
    songname = songname.replace(' ', '-')

    genius_url = f'https://genius.com/{artist}-{songname}-lyrics'
    return genius_url

def get_lyrics_from_genius_url(
    url : str, 
    title : bool = sc.INCLUDING_TITLE_CONSTANT, 
    one_line : bool = sc.ONE_LINE_CONSTANT
) -> any:
    '''
    args:
        url : the json file of songname, artist and URI
        title : title song
        one_line : True if return oneline lyric else list
    return:
        lyrics : text or list
    '''

    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    raw_lyrics = html.select('div[class*=Lyrics__Container]')

    lyrics = []
    for raw_lyric in raw_lyrics:
        lyric = re.sub(re.compile('<.*?>'), sc.SPECIAL_SYMBOL, str(raw_lyric)) # replace all texts inside <???> in '`'
        lyric = lyric.split(sc.SPECIAL_SYMBOL) # split with '`'
        lyric = [text.strip() for text in lyric] # in-case has 2 more space
        lyric = [text for text in lyric if text != ''] # remove space
        
        # merge some lyrics thats got splited with ','
        merge_lyric = []
        for text in lyric:
            text = text.replace('\u2005', ' ') # special case

            if not title and text[0] == '[': # remove [TITLE]
                continue
            
            if text[0] in sc.LOWER_ALPHABET:
                if text[0] != ',':
                    merge_lyric[-1] += ' '
                merge_lyric[-1] += text
                continue

            merge_lyric.append(text)
        
        lyrics += merge_lyric

    if one_line: # merge into one line
        lyrics = ' '.join(lyrics)

    return lyrics

def get_lyric_of_top_song(
    playlist_URI : str, 
    limit : int = sc.TOP_SONG_LIMIT_CONSTANT, 
    market : str = sc.MARKET_CONSTANT,
    title : bool = sc.INCLUDING_TITLE_CONSTANT, 
    one_line : bool = sc.ONE_LINE_CONSTANT
) -> list:
    '''
    args:
        playlist_URI : URI of spotify playlist
        limit : top song limit search
        market : region market song search
        title : title song
        one_line : True if return oneline lyric else list
    return:
        list of lyrics
    '''
    top_song_list = get_top_song_from_playlist(playlist_URI, limit=limit, market=market)

    lyrics = []
    for song in top_song_list:
        lyric = get_lyrics_from_genius_url(generate_genius_url(song), title=title, one_line=one_line)
        lyrics.append(lyric)

    return lyrics

if __name__ == '__main__':
    print(get_lyric_of_top_song('spotify:playlist:37i9dQZF1E4AfEUiirXPyP', limit=5))