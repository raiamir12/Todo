""" Todo Flask App """
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList
from app.resources.user import UserRegister, User
from app.config import POSTGRES_CONFIG
from app.db import db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
api = Api(app)

@app.before_first_request
def create_tables():
    """To Create Table in Database"""
    db.init_app(app)
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/login')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':

    app.run(debug=True)  # important to mention debug=True
