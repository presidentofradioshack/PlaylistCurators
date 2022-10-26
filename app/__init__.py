import asyncio
import os

import aiohttp
import requests
from flask import Flask, request
from googleapiclient.discovery import build

from app.spotify.api import SpotifyApi

from .google import *
from .util import StringUtil

app = Flask(__name__)

api = SpotifyApi(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

def extract_playlist_info(response: list) -> dict:
	playlists = []

	for playlist_group in response:
		items = playlist_group['playlists']['items']

		for playlist in items:
			email = StringUtil.check_string_for_email(playlist['description'])
			insta = StringUtil.check_string_for_insta(playlist['description'])

			if email or insta:
				playlists.append({
					'id': playlist['id'],
					'name': playlist['name'],
					'description': playlist['description'],
					'url': playlist['external_urls']['spotify'],
					'tracks': playlist['tracks']['total'],
					'owner': {
						'id': playlist['owner']['id'],
						'display_name': playlist['owner']['display_name'],
						'url': playlist['owner']['href'],
						'email': email,
						'insta': insta
					}
				})

	return playlists

async def get_recommendations(queries: list) -> list:
	async with aiohttp.ClientSession() as session:
		data = await get_all_queries(session, queries)
		results = extract_playlist_info(data)
		return results

async def get_all_queries(session: aiohttp.ClientSession, queries: list) -> list:
	tasks = []
	for query in queries:
		for offset in range(0, 1000, 50):
			task = asyncio.create_task(api.search_playlists_async(session, query, offset))
			tasks.append(task)
	
	results = await asyncio.gather(*tasks)
	return results

@app.route('/search')
def search():
	query = request.args.get('query')
	type = request.args.get('type')
	limit = request.args.get('limit')

	response = api.search(query, type, limit)

	items = response[f'{type}s']['items']
	return items

@app.route('/recommendations')
def recommendations() -> list:
	keyword = request.args.get('keyword')
	genres = request.args.get('genres')
	artist_ids = request.args.get('artists') 
	track_ids = request.args.get('tracks')

	primary_genre = genres.split(',')[0]

	if genres and artist_ids and track_ids:
		google_urls = []
		playlists = []

		recommendations = api.get_recommendations(artist_ids, primary_genre, track_ids, 5)
		for track in recommendations['tracks']:
			track_name = track['name']
			track_artist = track['artists'][0]['name']

			google_urls.append(build_search_url(track_name, track_artist))

		# if google_urls:
		# 	google_playlists = asyncio.run(get_playlists(google_urls))
		# 	playlists.extend(google_playlists)

		artists = []
		for id in artist_ids.split(','):
			artist = api.get_artist(id=id)
			artists.append(artist['name'])

		genres = genres.split(',')

		queries = [*artists, *genres]

		if keyword:
			queries.insert(0, keyword)

		results = asyncio.run(get_recommendations(queries=queries))
		playlists.extend(results)

		return playlists

if __name__ == '__main__':
	app.run()
