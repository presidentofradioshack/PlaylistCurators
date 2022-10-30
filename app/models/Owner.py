from dataclasses import dataclass

from marshmallow import Schema, fields
from app.database import db
from sqlalchemy import VARCHAR, Column, Integer, String
from sqlalchemy.orm import relationship

@dataclass
class Owner(db.Model):
	__tablename__ = 'owner'

	id = Column(Integer, primary_key=True)
	spotify_id = Column(String(40), unique=True)
	display_name = Column(String(128), nullable=False)
	url = Column(VARCHAR(128))
	email_address = Column(VARCHAR(128))
	instagram_handle = Column(VARCHAR(128))
	playlists = relationship('Playlist', back_populates='owner')

	def find_owner_by_id(id):
		owner = db.session.execute(
			db.select(Owner).filter_by(spotify_id = id)
		).scalars().first()

		return owner
	
class OwnerSchema(Schema):
	spotify_id = fields.Str()
	display_name = fields.Str()
	url = fields.Url()
	email_address = fields.Email()
	instagram_handle = fields.Str()