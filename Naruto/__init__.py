import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.' + os.getenv('FLASK_MODE', 'Development'))
app.config.from_pyfile(os.getenv('FLASK_MODE', 'Development') + '.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

from .visitor import visitor
app.register_blueprint(visitor)
from .admin import admin
app.register_blueprint(admin)


'''
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    #set the environment variable to alter the configruation
    #   export MODE='Production' 
    #           or 'Development' 
    #           or 'Testing' 
    #
    app.config.from_object('config.' + os.getenv('FLASK_MODE', 'Development'))
    app.config.from_pyfile(os.getenv('FLASK_MODE', 'Development') + '.py')

    db.init_app(app)
    migrate.init_app(app, db)

    #registe blueprint'
    from .visitor import visitor
    app.register_blueprint(visitor)
    from .admin import admin
    app.register_blueprint(admin)

    return app
'''


