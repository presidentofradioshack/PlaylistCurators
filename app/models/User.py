from dataclasses import dataclass
from app.database import db
from sqlalchemy import  BOOLEAN, VARCHAR, Column, DateTime, Integer


@dataclass
class User(db.Model):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(VARCHAR(128), nullable=False)
	email_address = Column(VARCHAR(256), unique=True, nullable=False)
	password = Column(VARCHAR(256), nullable=False)
	created_on = Column(DateTime, nullable=False)
	is_admin = Column(BOOLEAN, default=False, nullable=False)