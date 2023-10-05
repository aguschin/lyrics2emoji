from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

class SPOTIFY_CONSTANT:
    CID = 'd0c99630520f4f18bb353b2493728d85'
    SECRET_ID = '64c9b15c77244d2abbdf1796404178c4'

    CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(client_id=CID, client_secret=SECRET_ID)
    SPOTIFY = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

    URI = 'URI'
    ARTIST = 'Artist'
    SONGNAME = 'Songname'
    SPECIAL_SYMBOL = '`'
    TOP_SONG_LIMIT_CONSTANT = 10
    MARKET_CONSTANT = 'US'

    LOWER_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    INCLUDING_TITLE_CONSTANT = False
    ONE_LINE_CONSTANT = True