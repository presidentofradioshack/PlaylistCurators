from dataclasses import dataclass
from app.extensions import db
from sqlalchemy import JSON, Column, ForeignKey, Integer

@dataclass
class Usage_Statistic(db.Model):
	__tablename__ = 'usage_statistic'

	id = Column(Integer, primary_key=True)
	keywords = Column(JSON)
	genres = Column(JSON, nullable=False)
	artists = Column(JSON, nullable=False)
	songs = Column(JSON, nullable=False)
	user_id = Column(ForeignKey('user.id'))