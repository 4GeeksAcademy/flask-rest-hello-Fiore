from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email  # Cambiado 'username' a 'email'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    population = db.Column(db.Integer)
    description = db.Column(db.String(250))
    weather = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "description": self.description,
            "weather": self.weather,
            "url": self.url,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(25))
    eyes_color = db.Column(db.String(25))
    skin_color = db.Column(db.String(25))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "eyes_color": self.eyes_color,
            "skin_color": self.skin_color,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')  # Relación uno a muchos con User

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    planet = db.relationship('Planet')  # Relación uno a muchos con Planet

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    character = db.relationship('Character')  # Relacipn uno a muchos con Character

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
      return {
        "id": self.id,
        "user": self.user.serialize() if self.user else None,
        "planet": self.planet.serialize() if self.planet else None,
        "character": self.character.serialize() if self.character else None
    }
