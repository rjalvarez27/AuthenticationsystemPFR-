"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Role
from api.utils import generate_sitemap, APIException
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token


api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello mundo"
    }

    return jsonify(response_body), 200


#----------- Registro de usuario --------  

@api.route('/register', methods=['POST'])
def register():
    body = request.json 
    email = body.get('email', None)
    password = body.get('password', None)
    is_active = True
    role = body.get ("role", None) 
    if email is None or password is None:
        return {"error": "Campos requeridos"}, 400  
    if role not in Role.__members__:
        return{"error": f"{role} no existe"}    
    user_hash = generate_password_hash(password)        
    new_user = User(email=email, password=user_hash, is_active=is_active, role=role)    
    db.session.add(new_user)
    try:
       db.session.commit()
       return jsonify({"mesage":"Usuario Creado"}), 201
    except Exception as error:    
       db.session.rollback()    
       return {"error", error}, 500   

#------- login ---------
@api.route('/login', methods=["POST"])
def login():
    body = request.json
    email = body.get('email', None)
    password = body.get ("password", None)
    if email is None or password is None:
        return {"error": "Todos los campos son requeridos "}
    login_user = User.query.filter_by(email=email).first()    
    if check_password_hash(login_user.password, password):
        token = create_access_token({"id": login_user.id})
        print(token)
        return jsonify ({"access_token":token})
    else:     
        return "contrase;a incorrecta", 401

#-----Modificacion de la contrase;a------
@api.route('/change-password', methods=["PUT"])
def change_password():
    body= request.json
    email = body.get('email', None)
    new_email = body.get('new_email', None)
    password = body.get('password', None)
    if not email or not password:
        return{"error":"Todos los campos son necesarios"}
    update_user = User.query.filter_by(email=email).first()
    if not update_user:
        return {"error":"usuario no encontrado"}, 404    
    hash_password= generate_password_hash(password)
    update_user.password = hash_password
    update_user.email = new_email
    try:
        db.session.commit()
        return jsonify({"msg":"cambiando contrase;a o correo" }) 
    except Exception as error:    
        db.session.rollback()    
        return {"error": error}, 500  
