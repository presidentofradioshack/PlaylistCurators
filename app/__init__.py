import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.playlistfinder import playlist_finder_blueprint
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
	app = Flask(__name__)
	app.register_blueprint(playlist_finder_blueprint)
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
	from app.models import Artist, Owner, Playlist, Song, Usage_Statistic, User

	db.init_app(app)
	migrate.init_app(app, db)

	return app