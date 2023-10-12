import contextlib
import json
from pathlib import Path
from typing import TypedDict, List
from pprint import pprint

from bs4 import BeautifulSoup
import requests
import re
from spotify_constant import SPOTIFY_CONSTANT as sc


class Song(TypedDict):
    URI : str  # e.g. spotify:track:4HcARAxzsbIB3MqiEkejM6
    Artist : str
    Songname : str


def get_songname_artist_from_result(result):
    return {
        sc.URI : result['track']['uri'], 
        sc.ARTIST : result['track']['artists'][0]['name'],
        sc.SONGNAME : result['track']['name']
    }

def get_top_song_from_playlist(
    playlist_URI : str, 
    limit : int = sc.TOP_SONG_LIMIT_CONSTANT, 
    market : str = sc.MARKET_CONSTANT,
    offset: int = 0,
) -> list:
    '''
    get top N songs from the playlist

    args:
        playlist_URI : URI of spotify playlist
        limit : top song limit search
        market : region market song search
        offset: skip first n songs of the playlist
    return:
        list of songname, artist and URI as json
    '''
    results = sc.SPOTIFY.playlist_tracks(playlist_URI, limit=limit, market=market, offset=offset)

    list_of_song = []
    for song in results['items']:
        list_of_song.append(get_songname_artist_from_result(song))
    
    return list_of_song

def generate_genius_url(song_information : Song) -> str:
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
    songname = songname.replace('&', 'and') # special case
    
    # remove special alphabet
    songname = ''.join(char for char in songname if char.isalnum() or char == ' ')
    songname = songname.split(' ')
    songname = '-'.join([text for text in songname if text != ''])

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
        lyrics = '\n'.join(lyrics)
    return lyrics


class SongNormalised(TypedDict):
    song_name: str
    artist_name: str
    lyrics: str


def get_lyric_of_top_song(
        playlist_URI : str,
        limit : int = sc.TOP_SONG_LIMIT_CONSTANT,
        market : str = sc.MARKET_CONSTANT,
        title : bool = sc.INCLUDING_TITLE_CONSTANT,
        one_line : bool = sc.ONE_LINE_CONSTANT,
        first_n_song: int = 0,
        cache_filename: str = None,
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
    processed_songs = []
    processed_names = set()
    if cache_filename:
        try:
            with open(Path('data/sample_data/', cache_filename), 'r') as f:
                processed_songs = json.load(f)
        except FileNotFoundError:
            pass
    for song in processed_songs:
        processed_names.add(song['song_name'])
    first_n_song = limit if first_n_song == 0 else first_n_song
    res: List[Song] = []
    if first_n_song > 0:
        limit = 100 if first_n_song > 100 else first_n_song
    while first_n_song > 0:
        first_n_song -= limit
        top_song_list: List[Song] = get_top_song_from_playlist(playlist_URI, offset=len(res), limit=limit, market=market)
        res.extend(top_song_list)
    print(f'songs from spotify: {len(res)}')
    with_lyrics: List[SongNormalised] = []
    errors = 0
    for song in res:
        if song[sc.SONGNAME] in processed_names:
            continue
        try:
            lyric = get_lyrics_from_genius_url(generate_genius_url(song), title=title, one_line=one_line)
            with_lyrics.append({'song_name': song[sc.SONGNAME], 'artist_name': song[sc.ARTIST], 'lyrics': lyric})
            print(f'{len(with_lyrics)} songs processed.')
        except Exception as e:
            errors += 1
            print(f'Error: {e}. {errors} errors so far. Skipping song {song[sc.SONGNAME]} by {song[sc.ARTIST]}')
    return processed_songs + with_lyrics

def write_songs_to_json_file(filename, songs: List[SongNormalised]):
    path = Path('data/sample_data/', filename)
    with open(path, 'w') as f:
        json.dump(songs, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    songs_filename = 'top_300_spotify.json'
    res = get_lyric_of_top_song('spotify:playlist:7E3uEa1emOcbZJuB8sFXeK', first_n_song=350, cache_filename=songs_filename)
    write_songs_to_json_file(songs_filename, res)
    pprint(res)