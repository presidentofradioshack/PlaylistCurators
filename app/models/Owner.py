from dataclasses import dataclass
from app import db
from sqlalchemy import BOOLEAN, VARCHAR, Column, Integer, String
from sqlalchemy.orm import relationship

@dataclass
class Owner(db.Model):
	__tablename__ = 'owner'

	id = Column(Integer, primary_key=True)
	display_name = Column(String(128), nullable=False)
	url = Column(VARCHAR(128), nullable=False)
	email_address = Column(VARCHAR(128))
	instagram_handle = Column(VARCHAR(128))
	is_admin = Column(BOOLEAN)
	playlists = relationship('Playlist', back_populates='owner')