# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.schemas.user_schema import user_schema, users_schema, children_schema
from app.models.parent import Parent
from app.models.child import Child
from app import bcrypt
from sqlalchemy.exc import IntegrityError  
from flask_jwt_extended import create_access_token


signup_bp = Blueprint('signup_bp', __name__)


@signup_bp.route('/add_parent', methods=['POST'])
def add_parent():
    username = request.json['username']
    email = request.json['email']
    password_hash = bcrypt.generate_password_hash( request.json['password']).decode('utf-8')
    profile_picture = request.json['profile_picture']
    
    try:
        new_user = Parent(username, email, password_hash, profile_picture)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity={"email":email, "userType":"parent"})
        return jsonify(access_token=access_token), 200
    
    except IntegrityError as e :
        db.session.rollback()  # Rollback the transaction

        return jsonify({'message': 'Email is already taken'}), 400
    
    except Exception as e:
        db.session.rollback()

        return jsonify({'error': 'general', 'message': 'An unexpected error occurred'}), 500


@signup_bp.route('/users', methods=['GET'])
def get_users():
    all_users = Parent.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@signup_bp.route('/children', methods=['GET'])
def children():
    all_users = Child.query.all()
    result = children_schema.dump(all_users)
    return jsonify(result)


@signup_bp.route('/add_child', methods=['POST'])
def add_child():
    username = request.json['username']
    password_hash = bcrypt.generate_password_hash( request.json['password']).decode('utf-8')
    parent_nickname = request.json['parent_nickname']
    parent_id = request.json['parent_id']
    profile_picture = request.json['profile_picture']

    try:
        new_child = Child(username, password_hash, parent_nickname, parent_id, profile_picture)
        db.session.add(new_child)
        db.session.commit()
        return user_schema.jsonify(new_child)
    
    except IntegrityError as e :
        db.session.rollback()  # Rollback the transaction
        return jsonify({'message': 'username is already taken'}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'general', 'message': 'An unexpected error occurred'}), 500

    

