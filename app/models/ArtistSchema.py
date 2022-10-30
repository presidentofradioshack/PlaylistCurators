from app.extensions import ma
from app.models.Artist import Artist

class ArtistSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Artist
		include_relationships = True
		load_instance = True

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many = True)