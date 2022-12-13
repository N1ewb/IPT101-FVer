from app import app
from app import db
from posts.blueprint import posts
import views
from flask_migrate import Migrate, MigrateCommand
from flask.cli import FlaskGroup

app.register_blueprint(posts, url_prefix='/blog')
cli = FlaskGroup(app)
migrate = Migrate(app, db)

# The import Manager doesn't work, so I had to find another solution
cli.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()
