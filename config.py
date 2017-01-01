class Default:
    '''basic'''
    SECRET_KEY = 'your own secret key'

class Production(Default):
    '''SQLAlchemy'''
    SQLALCHEMY_DATABASE_URI = 'the correct URI to connect your own database'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Development(Default):
    '''basic'''
    DEBUG = True

    '''SQLAlchemy'''
    SQLALCHEMY_DATABASE_URI = 'the correct URI to connect your own database'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Testing(Default):
    '''basic'''
    TESTING = True

    '''SQLAlchemy'''
    SQLALCHEMY_DATABASE_URI = 'the correct URI to connect your own database'
    SQLALCHEMY_TRACK_MODIFICATIONS = True



