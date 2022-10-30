from app.extensions import ma
from app.models.Song import Song

class SongSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Song
		include_fk = True
		load_instance = True

song_schema = SongSchema()
songs_schema = SongSchema(many = True)