from dataclasses import dataclass
from app import db
from sqlalchemy import SMALLINT, VARCHAR, Column, ForeignKey, Integer, String

@dataclass
class Song(db.Model):
	__tablename__ = 'song'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String(40), unique=True, nullable=False)
	title = Column(VARCHAR(256), nullable=False)
	popularity = Column(SMALLINT)
	artist_id = Column(ForeignKey('artist.spotify_id'))