from dataclasses import dataclass
from app import db
from sqlalchemy import VARCHAR, Column, Integer, String
from sqlalchemy.orm import relationship

@dataclass
class Artist(db.Model):
	__tablename__ = 'artist'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String(40), unique=True, nullable=False)
	name = Column(VARCHAR(256), nullable=False)
	songs = relationship('Song')