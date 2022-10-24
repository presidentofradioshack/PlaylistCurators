import dotenv
import os
import urllib.parse
import requests
from urllib.parse import urlencode
from googleapiclient.discovery import build
from flask import Flask, request
from app.spotify.api import SpotifyApi
from .util import StringUtil

app = Flask(__name__)

dotenv.load_dotenv()

api = SpotifyApi(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

def extract_playlist_info(response):
	playlists = []
	items = response['playlists']['items']
	next = response['playlists']['next']
	offset = response['playlists']['offset']

	for playlist in items:
		email = StringUtil.check_string_for_email(playlist['description'])
		insta = StringUtil.check_string_for_insta(playlist['description'])

		if email or insta:
			playlists.append({
				'id': playlist['id'],
				'name': playlist['name'],
				'description': playlist['description'],
				'url': playlist['href'],
				'tracks': playlist['tracks']['total'],
				'owner': {
					'id': playlist['owner']['id'],
					'display_name': playlist['owner']['display_name'],
					'url': playlist['owner']['href'],
					'email': email,
					'insta': insta
				}
			})

	return {
		'playlists': playlists,
		'next': next,
		'offset': offset
	}

def request_playlists(search, next_url=None):
	results = []

	response = api.search(query=search, search_type='playlist', limit=50, next_url=next_url)
	playlist_info = extract_playlist_info(response=response)
	results.append(playlist_info['playlists'])

	return {
		'playlists': results,
		'next': playlist_info['next'],
		'offset': playlist_info['offset']
	}

@app.route('/search')
def search():
	query = request.args.get('query')
	type = request.args.get('type')
	limit = request.args.get('limit')

	response = api.search(query=query, search_type=type, limit=limit)

	items = response[f'{type}s']['items']
	return items

@app.route('/playlists/<search>')
def search_playlists(search):
	playlists = []
	next = True
	next_url = None
	offset = 0

	while (len(playlists) < 50) and next and offset < 1000:
		data = request_playlists(search=search, next_url=next_url)
		playlists.extend(data['playlists'])

		if data['next'] is None or data['offset'] == 1000:
			next = False
			next_url = None
		else:
			next_url = data['next']
			
		offset += 50
	return {
		'playlists': playlists
	}

@app.route('/categories')
def categories():
	response = api.get_categories()
	print(response)

	return {
		'categories': response
	}

@app.route('/recommendations')
def recommendations():
	keyword = request.args.get('keyword')
	genres = request.args.get('genres')
	artist_ids = request.args.get('artists')
	track_ids = request.args.get('tracks')

	artists = []
	for id in artist_ids.split(','):
		artist = api.get_artist(id=id)
		artists.append(artist['name'])

	if genres and artists and track_ids:
	# 	response = api.get_recommendations(seed_artists=artist_ids, seed_genres=genres, seed_tracks=track_ids)
	# 	api_key = os.getenv('API_KEY')
	# 	cx = os.getenv('SEARCH_ENGINE_ID')

		playlists = []
	# 	for track in response['tracks']:
	# 		artist = track['artists'][0]['name']
	# 		name = track['name']
	# 		page = 1
	# 		start = (page - 1) * 10 + 1
	# 		query_filter = f'inurl:open.spotify.com/playlist+intext:{name} {artist}'
	# 		query_string = urlencode({ 'q': query_filter, 'key': api_key, 'cx': cx, 'start': start})
	# 		endpoint = 'https://www.googleapis.com/customsearch/v1/siterestrict/'

	# 		url = f'{endpoint}?{query_string}'

	# 		data = requests.get(url).json()

	# 		for item in data['items']:
	# 			email = StringUtil.check_string_for_email(item['snippet'])
	# 			insta = StringUtil.check_string_for_insta(item['snippet'])
	# 			id = item['pagemap']['metatags']['og:url'].split('/')[0]
	# 			title = item['pagemap']['metatags']['og:title']
	# 			url = item['pagemap']['metatags']['og:url']

	# 			# if email or insta:
	# 			# 	playlists.append({
	# 			# 		'id': id,
	# 			# 		'name': item['name'],
	# 			# 		'description': item['description'],
	# 			# 		'url': item['href'],
	# 			# 		'owner': {
	# 			# 			'id': item['owner']['id'],
	# 			# 			'display_name': item['owner']['display_name'],
	# 			# 			'url': item['owner']['href'],
	# 			# 			'email': email,
	# 			# 			'insta': insta
	# 			# 		}
	# 			# 	})


	# 	return {}
		if keyword:
			offset = 0
			while offset < 1000:
				response = api.search_playlists(query=keyword, offset=offset)
				print(f'Keyword: {keyword} | Offset: {offset} | Playlists found: {len(playlists)}')
				playlist_info = extract_playlist_info(response=response)
				playlists.extend(playlist_info['playlists'])
				offset += 50

		for artist in artists:
			offset = 0
			while (offset < 1000):
				artist = artist.replace('-', ' ')
				print(f'Artist: {artist} | Offset: {offset} | Playlists found: {len(playlists)}')
				response = api.search_playlists(query=artist, offset=offset)
				playlist_info = extract_playlist_info(response=response)
				playlists.extend(playlist_info['playlists'])
				offset += 50
				
		for genre in genres.split(','):
			offset = 0
			while (offset < 1000):
				print(f'Genre: {genre} | Offset: {offset} | Playlists found: {len(playlists)}')
				genre = genre.replace('-', ' ')
				response = api.search_playlists(query=genre, offset=offset)
				playlist_info = extract_playlist_info(response=response)
				playlists.extend(playlist_info['playlists'])
				offset += 50

		return playlists


if __name__ == '__main__':
	app.run()