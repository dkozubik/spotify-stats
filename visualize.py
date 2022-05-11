import spotipy
from spotipy import SpotifyOAuth
import plotly.graph_objects as go
import plotly.subplots as sub
from statistics import mean


def run():
    figures = []
    spotify = authorize()
    show_user_top_tracks(spotify, figures, limit=10)
    show_user_top_artists(spotify, figures, limit=15)
    show_user_top_genres(spotify, figures, limit=7)
    show_user_playlists_summary(spotify, figures)
    show_figures(figures)


def authorize():
    """
    Add your <client_id>, <client_server>, <redirect_uri>
    and <username> developer spotify account's credentials or set them as environmental variables
    """
    client_id = ''
    client_secret = ''
    redirect_uri = ''
    username = ''

    scope = 'user-top-read playlist-read-private'

    token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope,
                         username=username)

    return spotipy.Spotify(auth_manager=token)


def show_user_top_tracks(spotify, figures, limit=10):
    top_tracks = spotify.current_user_top_tracks(limit=limit)
    res_list = []

    for track in top_tracks['items']:
        res_list.append((track['artists'][0]['name'], track['name']))

    col0 = list(range(1, len(res_list) + 1))
    col1 = [tmp[0] for tmp in res_list]
    col2 = [tmp[1] for tmp in res_list]

    table_obj = go.Table(
        columnorder=[1, 2, 3],
        columnwidth=[40, 400, 400],
        header=dict(values=['#', 'Artist', 'Track'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[col0, col1, col2],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='center',
                   font_size=15,
                   height=30
                   ))

    figures.append(table_obj)


def show_user_top_artists(spotify, figures, limit=10):
    top_artists = spotify.current_user_top_artists(limit=limit)
    res_list = []

    for artist in top_artists['items']:
        res_list.append(artist['name'])

    order = list(range(1, len(res_list) + 1))
    table_obj = go.Table(
        columnorder=[1, 2],
        columnwidth=[40, 400],
        header=dict(values=['#', 'Artist'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[order, res_list],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='center',
                   font_size=15,
                   height=30))

    figures.append(table_obj)


def show_user_top_genres(spotify, figures, limit=10):
    top_artists = spotify.current_user_top_artists(limit=50)
    genres_dic = dict()

    for artist in top_artists['items']:
        genres = artist['genres']
        for genre in genres:
            genres_dic[genre] = genres_dic.get(genre, 0) + 1

    genres_dic = dict(sorted(genres_dic.items(), key=lambda item: item[1], reverse=True))
    n_genres = list(genres_dic.items())[:limit]

    x_vals = [item[0] for item in n_genres]
    y_vals = [item[1] for item in n_genres]

    pie_obj = go.Pie(labels=x_vals, values=y_vals)
    figures.append(pie_obj)


def show_user_playlists_summary(spotify, figures):
    playlists = spotify.current_user_playlists()
    data = []  # (playlist name, tracks count, avg song duration, first song name)

    for playlist in playlists['items']:
        playlist_tracks = spotify.playlist_tracks(playlist_id=playlist['uri'])
        name = playlist['name']
        track_count = len(
            playlist_tracks['items'])  # Also, could use <playlist['total]> but it doesn't work on blend-type playlists
        avg_duration_seconds = round(mean([track['track']['duration_ms'] for track in playlist_tracks['items']]) / 1000,
                                     2)
        first_track = playlist_tracks['items'][0]['track']['name']

        data.append((name, track_count, avg_duration_seconds, first_track))

    col1 = [item[0] for item in data]
    col2 = [item[1] for item in data]
    col3 = [item[2] for item in data]
    col4 = [item[3] for item in data]

    table_obj = go.Table(
        header=dict(values=['Playlist', 'Total tracks', 'Average song duration (s)', 'The 1st song in the playlist'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[col1, col2, col3, col4],
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
        subplot_titles=("Your top tracks in the last 6 months", "Your top genres in the last 6 months",
                        "Your top artists in the last 6 months ", "Your playlists' brief summary")
    )

    fig.add_trace(figures[0], row=1, col=1)  # top tracks
    fig.add_trace(figures[1], row=2, col=1)  # top artists
    fig.add_trace(figures[2], row=1, col=2)  # top genres
    fig.add_trace(figures[3], row=2, col=2)  # playlists summary

    fig.update_layout(width=1200, height=1100)
    fig.show()


if __name__ == "__main__":
    run()
