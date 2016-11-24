import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
	app = Flask(__name__, instance_relative_config=True)

	'''set the environment variable to alter the configruation
	   export MODE='Production' 
				or 'Development' 
				or 'Testing' 
	'''
	app.config.from_object('config.' + os.getenv('MODE', 'Development'))
	app.config.from_pyfile(os.getenv('MODE', 'Development') + '.py')

	db = SQLAlchemy(app)

	'''registe blueprint'''
	from .visitor import visitor
	app.register_blueprint(visitor)
	from .admin import admin
	app.register_blueprint(admin)

	return app


