import asyncio
import os
import aiohttp
from flask import Blueprint, request
from app.spotify.api import *
from app.models.Artist import Artist
from app.models.Playlist import Playlist
from app.models.Owner import Owner
from app.models.Playlist import PlaylistSchema
from .google import *
from .util import StringUtil
from app.models.Song import Song
from app.database import db

playlist_finder_blueprint = Blueprint('playlist_finder_blueprint', __name__)

api = SpotifyApi(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

def extract_playlist_info(response: list):
	playlists = []

	for playlist_group in response:
		items = playlist_group['playlists']['items']

		for item in items:
			playlist = Playlist.find_playlist_by_id(item['id'])

			if playlist is None:
				email = StringUtil.check_string_for_email(item['description'])
				insta = StringUtil.check_string_for_insta(item['description'])

				if email or insta:
					playlist = Playlist()
					playlist.spotify_id = item['id']
					playlist.name = item['name']
					playlist.description = item['description']
					playlist.url = item['external_urls']['spotify']

					owner = Owner.find_owner_by_id(item['owner']['id'])
					if owner is None:
						owner = Owner()
						owner.spotify_id = item['owner']['id']
						owner.display_name = item['owner']['display_name']
						owner.email_address = email
						owner.instagram_handle = insta

						db.session.add(owner)
					
					owner.playlists.append(playlist)
					playlist.owner_id = owner.spotify_id
					db.session.add(playlist)
			
			if playlist is not None:
				playlists.append(playlist)
		
	db.session.commit()
	schema = PlaylistSchema(many=True)
	result = schema.dump(playlists)
	return result

async def get_recommendations(queries: list):
	async with aiohttp.ClientSession() as session:
		data = await get_all_queries(session, queries)
		results = extract_playlist_info(data)
		return results

async def get_all_queries(session: aiohttp.ClientSession, queries: list):
	tasks = []
	for query in queries:
		for offset in range(0, 1000, 50):
			task = asyncio.create_task(api.search_playlists_async(session, query, offset))
			tasks.append(task)
	
	results = await asyncio.gather(*tasks)
	return results

@playlist_finder_blueprint.route('/search')
def search():
	query = request.args.get('query')
	type = request.args.get('type')
	limit = request.args.get('limit')

	response = api.search(query, type, limit)

	items = response[f'{type}s']['items']
	return items

@playlist_finder_blueprint.route('/recommendations')
def recommendations():
	keyword = request.args.get('keyword')
	genres = request.args.get('genres')
	artist_ids = request.args.get('artists') 
	track_ids = request.args.get('tracks')

	primary_genre = genres.split(',')[0]

	if genres and artist_ids and track_ids:
		google_urls = []
		playlists = []

		recommendations = api.get_recommendations(artist_ids, primary_genre, track_ids, 50)

		new_songs = []
		new_artists = []
		for track in recommendations['tracks']:
			song = Song.find_song_by_id(track['id'])

			if song is None:
				song = Song()
				song.spotify_id = track['id']
				song.title = track['name']
				song.popularity = track['popularity']

				artist = Artist.find_artist_by_id(track['artists'][0]['id'])

				if artist is None:
					artist = Artist()
					artist.spotify_id = track['artists'][0]['id']
					artist.name = track['artists'][0]['name']
					new_artists.append(artist)
				
				artist.songs.append(song)
				song.artist_id = artist.spotify_id
				new_songs.append(song)
			else:
				matching_playlists = Playlist.find_playlists_by_song_id(song.spotify_id)

				if matching_playlists:
					playlists.extend(matching_playlists)
			

		db.session.add_all(new_artists)
		db.session.add_all(new_songs)
		db.session.commit()

		artists = []
		for id in artist_ids.split(','):
			artist = api.get_artist(id=id)
			artists.append(artist['name'])

		genres = genres.split(',')
		queries = [*artists, *genres]

		if keyword:
			queries.insert(0, keyword)

		results = asyncio.run(get_recommendations(queries))
		playlists.extend(results)

		return playlists