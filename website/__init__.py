from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_share import Share
from website.config import Config
 
SECRET_KEY = 'APNXGqHbrpAFfLpCnXy4Zg'
SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
share = Share()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    share.init_app(app)

    from website.user.routes import users
    from website.transcriptions.routes import transcripts
    from website.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(transcripts)
    app.register_blueprint(main)


    return app