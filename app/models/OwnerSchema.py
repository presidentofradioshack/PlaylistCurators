from app.extensions import ma
from app.models.Owner import Owner

class OwnerSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Owner
		include_relationships = True
		load_instance = True

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many = True)