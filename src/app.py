"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def hello_handle():
    users = User.query.all()
    if users == []:
      return jsonify({"msg": "Users doesn't exist" }), 404
    response_body = [user.serialize() for user in users]
    return jsonify(response_body), 200

@app.route('/users/<int:users_id>', methods=['GET'])
def get_users_id(users_id):
    user = User.query.filter_by(id=users_id).first()
    if user is None:
        return jsonify({"msg": "User doesn't exist" }), 404
    return jsonify(user.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planet = Planet.query.all()
    if planet == []:
        return jsonify({"msg": "Planets do not exist"}), 404
    response_body = [planet.serialize() for planet in planet]
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"msg": "Planet does not exist"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if characters == []:
        return jsonify({"msg": "Characters do not exist"}), 404
    response_body = [character.serialize() for character in characters]
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        return jsonify({"msg": "Character does not exist"}), 404
    return jsonify(character.serialize()), 200

@app.route('/favorite', methods=['GET'])
def get_favorite():
    favorites = Favorite.query.all()
    if favorites == []:
        return jsonify({"msg": "Favorites do not exist"}), 404
    response_body = [favorite.serialize() for favorite in favorites]
    return jsonify(response_body), 200


@app.route('/favorite/<int:favorite_id>', methods=['GET'])
def get_favorite_by_id(favorite_id):
    favorite = Favorite.query.filter_by(id=favorite_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite does not exist"}), 404
    return jsonify(favorite.serialize()), 200























# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
