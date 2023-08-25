import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta
from src.database.db_model import db
from src.database.Users import Users, LoginLog
from src.database.Images import Images
from src.database.GradeData import GradeData
from src.StorageManager import StorageManager

from flask_jwt_extended import JWTManager

storageManager = StorageManager()
class ReverseProxied(object):
    """
    Because we are reverse proxied from an aws load balancer
    use environ/config to signal https
    since flask ignores preferred_url_scheme in url_for calls
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # if one of x_forwarded or preferred_url is https, prefer it.
        forwarded_scheme = environ.get("HTTP_X_FORWARDED_PROTO", None)
        preferred_scheme = app.config.get("PREFERRED_URL_SCHEME", None)
        if "https" in [forwarded_scheme, preferred_scheme]:
            environ["wsgi.url_scheme"] = "https"
        return self.app(environ, start_response)

app = Flask(__name__, static_folder='build')
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.secret_key = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db" if os.environ.get("SERVER_TYPE") == "development" else os.getenv("POSTGRES_STRING")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)


# intialize flask restful api and enable CORS
api = Api(app)
CORS(app)

# intialize jwt manager
jwt = JWTManager(app)


db.init_app(app)
app.app_context().push()
db.create_all()

