from run import db
from passlib.hash import pbkdf2_sha256 as sha256
import jwt
from run import app
import uuid
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True) 
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(255))
    never_dies = db.Column(db.Boolean, default=False)

    def generate_public_id(self):
        self.public_id = str(uuid.uuid4())
        return self.public_id

    def generate_token(self, public_id, never_dies):
        self.token = jwt.encode({'public_id': public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'])
        db.session.commit()

    def hash_password(self, password):
        self.password = sha256.hash(password)
    
    def check_password(self, password):
        return sha256.verify(password, self.password)