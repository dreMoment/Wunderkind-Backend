# app/routes/login_routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, current_user
from app import db, bcrypt, login_manager
from app.models.parent import Parent
from app.models.child import Child
from app.routes.auth_service import AuthService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

login_bp = Blueprint('login_bp', __name__)


# User Loader callback
@login_manager.user_loader
def load_user(user_id):
    return Parent.query.get(int(user_id))

@login_bp.route('/login_parent', methods=['POST'])
def login():
    print("something")
    email = request.json['email']
    password = request.json['password']
    if AuthService.authenticate_parent(email, password):
        access_token = create_access_token(identity={"email":email, "userType":"parent"})
        
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401




@login_bp.route('/login_child', methods=['POST'])
def login_child():
    email = request.json['email']
    password = request.json['password']
    username = request.json['username']

    if AuthService.authenticate_child(email,username, password):
        access_token = create_access_token(identity={"email":email, "userType":"child", "username":username})
        
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401



@login_bp.route('/show_tutorial/<int:user_id>', methods=['GET'])
@jwt_required()
def show_tutorial(user_id):
    current_user_identification = get_jwt_identity()
    user_type = current_user_identification['userType']
    user_email = current_user_identification['email']

    parent = Parent.query.filter_by(email=user_email).first()
    if not parent:
        return jsonify({'message': 'Parent not found'}), 404

    if user_type == "parent" and user_id == parent.id:
        return jsonify({'show_tutorial': parent.show_tutorial}), 200
    
    elif user_type == "child":
        child = Child.query.filter_by(parent_id=parent.id, id=user_id).first()
        if child:
            return jsonify({'show_tutorial': child.show_tutorial}), 200

    return jsonify({'message': 'Invalid usertype or permission denied'}), 401


@login_bp.route('/set_show_tutorial_false/<int:user_id>', methods=['PUT'])
@jwt_required()
def set_show_tutorial_false(user_id):
    current_user_identification = get_jwt_identity()
    user_type = current_user_identification['userType']
    user_email = current_user_identification['email']

    parent = Parent.query.filter_by(email=user_email).first()
    if not parent:
        return jsonify({'message': 'Parent not found'}), 404

    if user_type == "parent" and user_id == parent.id:
        parent.show_tutorial = False
        db.session.commit()
        return jsonify({'message': 'Parent show_tutorial set to False'}), 200
    
    elif user_type == "child":
        child = Child.query.filter_by(parent_id=parent.id, id=user_id).first()
        if child:
            child.show_tutorial = False
            db.session.commit()
            return jsonify({'message': 'Child show_tutorial set to False'}), 200

    return jsonify({'message': 'Invalid usertype or permission denied'}), 401
