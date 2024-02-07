import os
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth

#This class is responsible for handling all data related to Spotify and communicating with the Spotify API.

class SpotifyDataOperations:
    def __init__(self):
        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")
        self.scope = 'playlist-modify-private'
        self.auth_manager = SpotifyOAuth(client_id=self.client_id,
            client_secret=self.client_secret,
                                         scope=self.scope,
                                         redirect_uri="http://example.com")
        self.access_token = self.auth_manager.get_access_token()['access_token']
        self.endpoint = "https://api.spotify.com/v1/"

        self.header = {
            "Authorization": f"Bearer {self.access_token}"
        }

        self.client = spotipy.Spotify(auth_manager=self.auth_manager)
        self.user = self.client.current_user()['id']


    def spotify_search(self, song, year):
        response = self.client.search(
            q=f"{song},{year}", type="track", market="US", offset=0)
        return response

    def create_playlist(self, date, uri_list):
        playlist_create_endpoint = self.endpoint + f"users/{self.user}/playlists"
        playlist_params = self.get_playlist_params(date)

        my_playlist = requests.post(url=playlist_create_endpoint, json=playlist_params, headers=self.header, timeout=60)
        my_playlist_json = my_playlist.json()

        my_playlist_id = my_playlist_json['id']
        playlist_add_endpoint = self.endpoint + f"playlists/{my_playlist_id}/tracks"

        playlist_add_params = self.get_playlist_add_params(uri_list)

        playlist_reponse = requests.post(
            url=playlist_add_endpoint, json=playlist_add_params, headers=self.header, timeout=60)
        return playlist_reponse


    def get_playlist_params(self, date):
        parameters = {
            "name": f"{date} Billboard Top 100",
            "description": f"Billboard Top 100 songs in {date}.",
            "public": False
        }
        return parameters

    def get_playlist_add_params(self, uri_list):
        parameters = {
            "uris": uri_list,
            "position": 0
        }
        return parameters
