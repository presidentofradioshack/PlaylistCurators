from dataclasses import dataclass
from app.extensions import db, ma
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.Song_In_Playlist import song_in_playlist

@dataclass
class Playlist(db.Model):
	__tablename__ = 'playlist'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String(40), unique=True, nullable=False)
	name = Column(VARCHAR(200), nullable=False)
	description = Column(VARCHAR(300))
	url = Column(VARCHAR(128), nullable=False)
	owner_id = Column(ForeignKey('owner.spotify_id'), nullable=False)
	songs = relationship('Song', secondary=song_in_playlist)
	owner = relationship('Owner', back_populates='playlists')

	def find_playlist_by_id(id):
		playlist = db.session.execute(
			db.select(Playlist).filter_by(spotify_id = id)
		).scalars().first()

		return playlist

	def find_playlists_by_song_id(id):
		playlists = db.session.execute(
			db.select(Playlist)\
				.join(song_in_playlist)\
				.filter(song_in_playlist.c.song_id == id)
		).scalars().all()

		return playlists