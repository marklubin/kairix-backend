from flask  import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/chatdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    migrate.init_app(app, db)

    db.init_app(app)

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app