from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

authorizations = {
    'JWT': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(app, security=['JWT'], authorizations=authorizations)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    from core.models import User
    db.create_all()

jwt = JWTManager(app)


from core import routes