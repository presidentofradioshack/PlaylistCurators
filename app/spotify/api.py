import base64
from cgitb import lookup
import datetime
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
import requests

class SpotifyApi(object):
	access_token = None
	access_token_expires = datetime.datetime.now()
	access_token_expired = True
	client_id = None
	client_secret = None
	token_url = 'https://accounts.spotify.com/api/token'

	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret

	def authenticate_token(self):
		token_url = self.token_url
		token_data = self.get_token_data()
		token_headers = self.get_token_headers()

		response = requests.post(token_url, data=token_data, headers=token_headers)

		if response.status_code not in range(200, 299):
			return False

		data = response.json()

		now = datetime.datetime.now()
		self.access_token = data['access_token']
		expires_in = data['expires_in']
		self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
		self.access_token_expired = self.access_token_expires < now

		return True

	def get_access_token(self):
		token = self.access_token
		expires = self.access_token_expires
		now = datetime.datetime.now()
		if expires < now or token is None:
			self.authenticate_token()
			return self.get_access_token()

		return token

	def get_client_credentials(self):
		client_id = self.client_id
		client_secret = self.client_secret

		if client_secret is None or client_id is None:
			raise Exception('You must set client_id and client_secret')

		client_credentials = f'{client_id}:{client_secret}'
		client_credentials_encoded = base64.b64encode(client_credentials.encode('ascii'))

		return client_credentials_encoded.decode('ascii')

	def get_token_headers(self):
		client_credentials_encoded = self.get_client_credentials()

		return {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': f'Basic {client_credentials_encoded}'
		}

	def get_token_data(self):
		return {
			'grant_type': 'client_credentials'
		}

	def get_resource_headers(self):
		access_token = self.get_access_token()

		return {
			'Accept': 'application/json',
			'Authorization': f'Bearer {access_token}',
			'Content-Type': 'application/json'
		}

	def handle_response(response):
		if response.status_code not in range(200, 299):
			return {
				'Status': response.status_code
			}

		data = response.json()

		return data
	
	def search(self, query, search_type='artists', limit=50, offset=0, next_url=None):
		if next_url:
			lookup_url = next_url
		else:
			endpoint = 'https://api.spotify.com/v1/search'
			query_string = urlencode({ 'q': query, 'type': search_type.lower(), 'limit': limit, 'offset': offset })

			lookup_url = f'{endpoint}?{query_string}'

		response = requests.get(lookup_url, headers=self.get_resource_headers())

		if response.status_code not in range(200, 299):
			return {
				'Status': response.status_code
			}

		data = response.json()

		return data
		
	def search_artists(self, query):
		return self.search(query=f'artist:{query}', search_type='artist')

	def search_playlists(self, query, offset=0):
		return self.search(query=query, search_type='playlist', offset=offset)

	def get_artist(self, id):
		endpoint = f'https://api.spotify.com/v1/artists/{id}'

		response = requests.get(endpoint, headers=self.get_resource_headers())
		if response.status_code not in range(200, 299):
			return {
				'Status': response.status_code
			}

		data = response.json()

		return data

	def get_categories(self, limit=0, offset=0):
		endpoint = 'https://api.spotify.com/v1/browse/categories'
		query_string = urlencode({ 'limit': limit, 'offset': offset })

		lookup_url = f'{endpoint}?{query_string}'

		response = requests.get(lookup_url, headers=self.get_resource_headers())

		if response.status_code not in range(200, 299):
			return {
				'Status': response.status_code
			}

		data = response.json()

		return data

	def get_genre_seeds(self):
		endpoint = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'

		response = requests.get(endpoint, headers=self.get_resource_headers())

		if response.status_code not in range(200, 299):
			return {
				'Status': response.status_code
			}

		data = response.json()

		return data

	def get_recommendations(self, seed_artists=None, seed_genres=None, seed_tracks=None, limit=50):
		if (seed_artists is None or seed_genres is None or seed_tracks is None):
			return False

		endpoint = 'https://api.spotify.com/v1/recommendations'
		query_string = urlencode({ 'seed_artists': seed_artists, 'seed_genres': seed_genres, 'seed_tracks': seed_tracks, 'limit': limit })

		lookup_url = f'{endpoint}?{query_string}'

		response = requests.get(lookup_url, headers=self.get_resource_headers())

		if response.status_code not in range(200, 299):
			return {
				'Status': response.status_code
			}

		data = response.json()

		return data

