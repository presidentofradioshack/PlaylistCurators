import asyncio
import json
import os
from urllib.parse import urlencode

import aiohttp

from .util import StringUtil


async def get_playlists(urls: list) -> list:
	async with aiohttp.ClientSession() as session:
		data = await create_tasks(session, urls)
		
		results = extract_playlist_info(data)
		return results

async def create_tasks(session: aiohttp.ClientSession, urls: list) -> list:
	tasks = []
	for url in urls:
		tasks.append(asyncio.create_task(google_search(session, url)))
	
	results = await asyncio.gather(*tasks)
	return results

def build_search_url(track: str, artist: str):
	api_key = os.getenv('API_KEY')
	cx = os.getenv('SEARCH_ENGINE_ID')
	page = 1
	start = (page - 1) * 10 + 1
	query_filter = f'(insta OR @ OR instagram OR email OR submissions OR submit OR request OR requests OR suggestions OR follow me OR follow my OR placements) -utm_source=instagram inurl:open.spotify.com/playlist+intext:{track} {artist}'
	query_string = urlencode({ 'q': query_filter, 'key': api_key, 'cx': cx, 'start': start})
	endpoint = 'https://www.googleapis.com/customsearch/v1/siterestrict/'
	
	url = f'{endpoint}?{query_string}'

	return url

async def google_search(session: aiohttp.ClientSession, url: str):
	async with session.get(url) as response:
		return await response.json()
	
def extract_playlist_info(response):
	playlists = []
	for group in response:
		if group['searchInformation']['totalResults'] != '0':
			for item in group['items']:
				email = StringUtil.check_string_for_email(item['snippet'])
				insta = StringUtil.check_string_for_insta(item['snippet'])

				if email or insta:
					id = item['link'].split('/')[-1]
					name = item['pagemap']['metatags'][0]['og:title']
					url = item['link']
					display_name = item['pagemap']['metatags'][0]['og:description'].split('·')[0].strip()
					
					playlists.append({
						'id': id,
						'name': name,
						'url': url,
						'owner': {
							'id': display_name,
							'display_name': display_name,
							'email': email,
							'insta': insta
						}
					})
	
	return playlists
