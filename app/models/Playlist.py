from dataclasses import dataclass
from app import db
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
	owner_id = Column(ForeignKey('owner.id'), nullable=False)
	songs = relationship('Song', secondary=song_in_playlist, back_populates='playlist')
	owner = relationship('Owner', back_populates='playlists')