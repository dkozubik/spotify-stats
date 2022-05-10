import spotipy
from spotipy import SpotifyOAuth


def run():
    authorize()

def authorize():

    client_id = ''
    client_secret = ''
    redirect_uri = ''

    scope = 'playlist-modify-private user-read-private user-library-read user-top-read playlist-read-private'
    username = ''

    token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope,
                         username=username)

    return spotipy.Spotify(auth_manager=token)

if __name__ == "__main__":
    run()