
from main import app, db ,Product, ProductUser
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict (app=app, db=db, Product=Product, ProductUser=ProductUser)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
