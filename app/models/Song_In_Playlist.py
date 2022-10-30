from sqlalchemy import Column, ForeignKey
from app.database import db

song_in_playlist = db.Table(
	'song_in_playlist',
	Column('playlist_id', ForeignKey('playlist.spotify_id')),
	Column('song_id', ForeignKey('song.spotify_id')),
)