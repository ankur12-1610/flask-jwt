from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.TokenGenerate, '/<public_id>/token/generate')
api.add_resource(resources.RefreshToken, '/<public_id>/token/refresh')
api.add_resource(resources.DeleteToken, '/<public_id>/token/delete')
api.add_resource(resources.GetCurrentToken, '/<public_id>/token/current')


if __name__ == '__main__':
    db.create.all()
    app.run(debug=True)