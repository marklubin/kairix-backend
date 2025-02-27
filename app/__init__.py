from app.config import get_config
from flask  import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    migrate.init_app(app, db)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes.users import users_bp
    from .routes.agents import agents_bp
    from .routes.messages import messages_bp
    from .routes.conversations import conversations_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(conversations_bp, url_prefix='/api/conversations')   

    return app