import os
from flask import Flask
from app.extensions import db, migrate, ma
from app.playlistfinder import playlist_finder_blueprint
from dotenv import load_dotenv

load_dotenv()

def create_app():
	app = Flask(__name__)
	app.register_blueprint(playlist_finder_blueprint)
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
	from app.models import Artist, Owner, Playlist, Song, Song_In_Playlist, Usage_Statistic, User

	db.init_app(app)
	ma.init_app(app)
	migrate.init_app(app, db, render_as_batch=True)

	return app