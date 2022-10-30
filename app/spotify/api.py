import requests
from urllib.parse import urlencode
from app.spotify.auth import SpotifyAuth

class SpotifyApi():
	def __init__(self, client_id, client_secret):
		self.authenticator = SpotifyAuth(client_id=client_id, client_secret=client_secret)

	def get_resource_headers(self):
		access_token = self.authenticator.get_access_token()

		return {
			'Accept': 'application/json',
			'Authorization': f'Bearer {access_token}',
			'Content-Type': 'application/json'
		}
	
	def search(self, query: str, search_type: str='artists', limit: int=50, offset: int=0, next_url: str=None) -> dict:
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

	async def search_async(self, session, query, search_type='artists', limit=50, offset=0):
		if query:
			endpoint = 'https://api.spotify.com/v1/search'
			query_string = urlencode({ 'q': query, 'type': search_type.lower(), 'limit': limit, 'offset': offset })

			lookup_url = f'{endpoint}?{query_string}'

			async with session.get(lookup_url, headers=self.get_resource_headers()) as response:
				if response.status not in range(200, 299):
					return {
						'Status': response.status,
						'URL': lookup_url
					}

				return await response.json()
		
	async def search_artists(self, query):
		return await self.search(query=f'artist:{query}', search_type='artist')

	def search_playlists(self, query, offset=0):
		return self.search(query=query, search_type='playlist', offset=offset)

	async def search_playlists_async(self, session, query, offset=0):
		return await self.search_async(session, query=query, search_type='playlist', offset=offset)

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

	def get_recommendations(self, seed_artists=None, seed_genres=None, seed_tracks=None, limit=10):
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