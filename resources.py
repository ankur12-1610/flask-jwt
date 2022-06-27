from lib2to3.pgen2 import token
from flask import Flask
from flask_restful import Api, abort, reqparse, Resource
from models import *
import uuid
import jwt
import datetime
from run import app
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    return True

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('never_dies', type=bool, required=False)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        user = User(**data)
        user.generate_public_id()
        user.hash_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User named {} created successfully'.format(data['username'])}, 201

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'User does not exist'}, 400
        if user.check_password(data['password']):
            return {'user' : user.username, 'public_id': user.public_id, 'token': user.token}, 200
        return {'message': 'Wrong password'}, 401

class GetCurrentToken(Resource):
    @auth.login_required
    def get(self, public_id):
        data = parser.parse_args()
        user = User.query.filter_by(username = data['username']).first()
        if not user.token:
            return {'message': 'Token does not exist'}, 400
        return {'token': user.token, "never_dies": user.never_dies }, 200
class TokenGenerate(Resource):
    @auth.login_required
    def post(self, public_id):
        data = parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        if user.token:
            return {'message': 'Token already exists'}, 400
        user.generate_token(public_id, never_dies = data['never_dies'])
        db.session.commit()
        return {'token': user.token}, 201

class RefreshToken(Resource):
    @auth.login_required
    def get(self, public_id):
        data = parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        user.generate_token(public_id, never_dies = data['never_dies'])
        db.session.commit()
        return {'token': user.token}

class DeleteToken(Resource):
    @auth.login_required
    def get(self, public_id):
        data = parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        user.token = None
        db.session.commit()
        return {'message': 'Token deleted'}