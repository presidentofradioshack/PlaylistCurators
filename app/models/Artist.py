from dataclasses import dataclass
from app.extensions import db
from sqlalchemy import VARCHAR, Column, Integer, String
from sqlalchemy.orm import relationship

@dataclass
class Artist(db.Model):
	__tablename__ = 'artist'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String(40), unique=True, nullable=False)
	name = Column(VARCHAR(256), nullable=False)
	songs = relationship('Song', back_populates='artist')

	def find_artist_by_id(id):
		artist = db.session.execute(
			db.select(Artist).filter_by(spotify_id = id)
		).scalars().first()

		return artist