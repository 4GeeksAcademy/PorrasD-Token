"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)
bcrypt=Bcrypt()
jwt=JWTManager()
delete_tokens = set() 

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods = ['POST'])
def sign_up():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user_exists = User.query.filter_by(email = email).first()

    if user_exists is None:
        password_hash =  bcrypt.generate_password_hash(password)

        new_user = User(
            name = name,
            email = email,
            password = password_hash,
            is_active = True
        )        

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return jsonify({"message": "An error has ocurred."}), 500

        return jsonify({
            "user": new_user.serialize(),
            "message": "You have registered! Redirecting to log-in page" 
        }), 200
    else:
        return jsonify({"message": "Email already in use. Try using another one."}), 400
    
@api.route('/login', methods = ['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_exists = User.query.filter_by(email = email).first()

    if user_exists:
        valid_password = bcrypt.check_password_hash(user_exists.password, password)
        if valid_password:
            access_token = create_access_token(identity=user_exists.email)
            return jsonify({"token": access_token}), 200  
        else:
            return jsonify({"message": "Invalid password."}), 401 
    else:
        return jsonify({"message": "Invalid user."}), 404
    
# @api.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]  
#     delete_tokens.add(jti)   
#     return jsonify({"msg": "You have been logged-out"}), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    jti = get_jwt()["jti"]
    if jti in delete_tokens:
        return jsonify({"msg": "Token has been revoked."}), 401  

    email = get_jwt_identity()
    user_exists = User.query.filter_by(email=email).first()
    return jsonify(user_exists.serialize()), 200