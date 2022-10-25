import dotenv
import os
import urllib.parse
import requests
import json
from pprint import pp
import asyncio
import aiohttp
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

	for playlist_group in response:
		items = playlist_group['playlists']['items']
		next = playlist_group['playlists']['next']
		offset = playlist_group['playlists']['offset']

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


async def get_recommendations(queries: list) -> list:
	async with aiohttp.ClientSession() as session:
		data = await get_all_queries(session=session, queries=queries)
		return data

async def get_all_queries(session: aiohttp.ClientSession, queries: list) -> list:
	tasks = []
	for query in queries:
		for offset in range(0, 1000, 50):
			task = asyncio.create_task(api.search_playlists_async(session=session, query=query, offset=offset))
			tasks.append(task)
	
	results = await asyncio.gather(*tasks)
	return results

@app.route('/recommendations')
def recommendations():
	keyword = request.args.get('keyword')
	genres = request.args.get('genres')
	artist_ids = request.args.get('artists') 
	track_ids = request.args.get('tracks')

	genres = genres.split(',')

	if genres and artist_ids and track_ids:
		artists = []
		for id in artist_ids.split(','):
			artist = api.get_artist(id=id)
			artists.append(artist['name'])

		playlists = []

		queries = [keyword, *artists, *genres]

		results = asyncio.run(get_recommendations(queries=queries))
		
		playlists.extend(results)
		data = extract_playlist_info(playlists)

		return data['playlists']

if __name__ == '__main__':
	app.run()