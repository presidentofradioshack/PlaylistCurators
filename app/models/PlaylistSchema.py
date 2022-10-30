from app.extensions import ma
from app.models.Playlist import Playlist
from app.models.Owner import Owner
from app.models.OwnerSchema import OwnerSchema

class PlaylistSchema(ma.SQLAlchemyAutoSchema):
	owner = ma.Nested(OwnerSchema)

	class Meta:
		model = Playlist
		include_fk = True
		load_instance = True

playlist_schema = PlaylistSchema()
playlists_schema = PlaylistSchema(many = True)