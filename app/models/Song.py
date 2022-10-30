from dataclasses import dataclass
from app.extensions import db, ma
from sqlalchemy import SMALLINT, VARCHAR, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

@dataclass
class Song(db.Model):
	__tablename__ = 'song'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String(40), unique=True, nullable=False)
	title = Column(VARCHAR(256), nullable=False)
	popularity = Column(SMALLINT)
	artist_id = Column(ForeignKey('artist.spotify_id'))
	artist = relationship('Artist', back_populates='songs')

	def find_song_by_id(id):
		song = db.session.execute(
			db.select(Song).filter_by(spotify_id = id)
		).scalars().first()

		return song