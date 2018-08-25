# -*- coding: utf-8 -*-

# WORK IN PROGRESS

import locale
import time
from dateutil import parser
import requests

VAL202_API = 'https://val202.rtvslo.si/api/nowplaying'
YOUTUBE_SEARCH_URL = 'https://www.youtube.com/results'

def main():
    _set_locale()

    current_song_id = None
    while True:
        response = requests.get(VAL202_API)
        if response.status_code != 200:
            time.sleep(10)
            continue

        try:
            latest_song = response.json()['data'][0]
        except (KeyError, IndexError) as e:
            # TODO
            print(e)
            exit(1)

        if latest_song['id'] == current_song_id:
            time.sleep(10)
            continue

        current_song_id = latest_song['id']
        attributes = latest_song['attributes']
        start_time = parser.parse(attributes['start-time'])
        artist = attributes['artist-name']
        song_title = attributes['title-name']
        url = _get_youtube_search_url(artist, song_title)
        print(url)

def _set_locale():
    try:
        locale.setlocale(locale.LC_TIME, "sl_SI.utf8")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, "sl_SI")  # osx
        except locale.Error as e:
            # TODO
            print(e)
            exit(1)

def _get_youtube_search_url(artist, song_title):
    params = {'search_query': '{} {}'.format(artist, song_title)}
    return requests.Request('GET', YOUTUBE_SEARCH_URL, params=params).prepare().url


if __name__ == '__main__':
    main()
