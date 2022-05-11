# spotify-stats
This application shows a user their top tracks & artists & genres in the last 6 months and a brief stats summary of their playlists.

## Obtaining credentials
First, you need to have a Spotify account. If so, sign in [here](https://developer.spotify.com/dashboard/). Then, click on *CREATE AN APP* and fill a form. Here you will need **Client ID** and **Client secret** later. Moreover, click on *EDIT SETTINGS* and fill in at least one **Redirect URIs**, which can be any URL and save the settings.

## Usage
Run with
```bash
python visualize.py
```
You will be prompted to fill your:
- Client ID
- Client secret
- Redirect URI -> must be one of the previously filled in the App settings
- Spotify username -> your Spotify account username, if you are logged via Facebook, a username is usually a generated alphanumeric string

In addition, at the initial startup, you might be asked to enter a URL you were redirected to, due to authentication process. Simply, copy and paste that address.
