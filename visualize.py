import spotipy
from spotipy import SpotifyOAuth
import plotly.graph_objects as go
import plotly.subplots as sub


def run():
    figures = []
    spotify = authorize()
    show_user_top_tracks(spotify, figures)
    show_figures(figures)


def authorize():
    """
    Add your <client_id>, <client_server>, <redirect_uri>
    and <username> credentials or set them as environmental variable
    """
    client_id = ''
    client_secret = ''
    redirect_uri = ''
    username = ''

    scope = 'playlist-modify-private user-read-private user-library-read user-top-read playlist-read-private'

    token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope,
                         username=username)

    return spotipy.Spotify(auth_manager=token)


def show_user_top_tracks(spotify, figures):
    top_tracks = spotify.current_user_top_tracks(limit=10)

    res_list = []
    for track in top_tracks['items']:
        res_list.append((track['artists'][0]['name'], track['name']))

    col1 = [tmp[0] for tmp in res_list]
    col2 = [tmp[1] for tmp in res_list]

    table_obj = go.Table(
        header=dict(values=['Artist', 'Track'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[col1, col2],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='center',
                   font_size=15,
                   height=30
                   ))

    figures.append(table_obj)


def show_figures(figures):
    fig = sub.make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "table"}, {"type": "pie"}],
               [{"type": "table"}, {"type": "table"}]],
        subplot_titles=("Your top 10 tracks in the last 6 months", "Your top 10 genres in the last 6 months",
                        "Your top 10 artists in the last 6 months ", "Your playlists' brief summary")
    )

    fig.add_trace(figures[0], row=1, col=1)  # top 10 tracks
    fig.show()


if __name__ == "__main__":
    run()
