from Naruto import app, models
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0'), port=5000)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
