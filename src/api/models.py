from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class Role(enum.Enum):
   admin = "admin"
   user = "user"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False , default="admin")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }