# app/routes/login_routes.py
from flask import Blueprint, request, jsonify
from app import db, bcrypt, login_manager
from app.models.parent import Parent
from app.models.child import Child
from app import bcrypt
from app.routes.auth_service import AuthService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError  

user_bp = Blueprint('user_bp', __name__)



@user_bp.route('/get_user_id', methods=['GET'])
@jwt_required()
def get_user_id():
    current_user_identity = get_jwt_identity()
    current_user_email = current_user_identity['email']
    current_user_type = current_user_identity['userType']

    if current_user_type == 'parent':
        user = Parent.query.filter_by(email=current_user_email).first()

    elif current_user_type == 'child':
        username = current_user_identity['username']
        parent = Parent.query.filter_by(email=current_user_email).first()
        user = Child.query.filter_by(parent_id=parent.id, username=username).first()

    if user:
        return jsonify(user_id=user.id), 200
    else:
        return jsonify({"msg": "User not found"}), 404


@user_bp.route('/get_user_type', methods=['GET'])
@jwt_required()
def get_user_type():
    current_user_identity = get_jwt_identity()

    if 'userType' in current_user_identity:
        return jsonify({'userType': current_user_identity['userType']}), 200
    else:
        return jsonify({'error': 'User type not found in token'}), 400


@user_bp.route('/get_profile_pic/<user_type>/<int:id>', methods=['GET'])
@jwt_required()
def get_profile_picture(user_type, id):

    if user_type == 'parent':
        user = Parent.query.get(id)
        if user:
            return jsonify({"profile_pic": user.profile_picture})
        else:
            return jsonify({"msg": "Parent not found"}), 404


    elif user_type == "child":
        user = Child.query.get(id)
        if user:
            return jsonify({"profile_pic": user.profile_picture})
        else:
            return jsonify({"msg": "Child not found"}), 404

    else:
        return jsonify({"msg": "Invalid user type"}), 400



@user_bp.route('/get_username/<user_type>/<int:id>', methods=['GET'])
@jwt_required()
def get_username(user_type, id):

    if user_type == 'parent':
        user = Parent.query.get(id)
        if user:
            return jsonify({"username": user.name})
        else:
            return jsonify({"msg": "Parent not found"}), 404


    elif user_type == "child":
        user = Child.query.get(id)
        if user:
            return jsonify({"username": user.username})
        else:
            return jsonify({"msg": "Child not found"}), 404

    else:
        return jsonify({"msg": "Invalid user type"}), 400




@user_bp.route('/edit_username/<user_type>/<int:id>', methods=['POST'])
@jwt_required()
def edit_username(user_type, id):
    current_user_identification = get_jwt_identity()
    email = current_user_identification['email']
    data = request.json
    new_username = data.get("username")
    if not new_username:
        return jsonify({"msg": "No new username provided"}), 400

    if user_type == "child":
        authorised_child = AuthService.is_authorised_for_child(id)
        if not authorised_child:
            return jsonify({"msg": "Unauthorized access"}), 403
        
        try:

            authorised_child.username = new_username
            db.session.commit()
            new_token = create_access_token(identity={"email":email, "userType":"child", "username":new_username})

            return jsonify({
                    "msg": "Username updated successfully",
                    "new_token": new_token}), 200 
               
        except IntegrityError as e :
            db.session.rollback()  # Rollback the transaction
            return jsonify({'msg': 'username is already taken'}), 400
    
        except Exception as e:
            return jsonify({"msg": str(e)}), 400

    elif user_type == "parent":
        curr_user = get_jwt_identity()
        parent = Parent.query.get(id)
        if parent and parent.email == curr_user['email']:
            try:
                parent.name = new_username
                db.session.commit()
                return jsonify({"msg": "Username updated successfully"}), 200
        
            except Exception as e:
                return jsonify({"msg": str(e)}), 400
            
    else:
        return jsonify({"msg": "Invalid user type"}), 400



@user_bp.route('/edit_parent_nickname/<int:id>', methods=['POST'])
@jwt_required()
def edit_parent_nickname(id):
    data = request.json
    new_nickname = data.get("nickname")
    if not new_nickname:
        return jsonify({"msg": "No new username provided"}), 400

    authorised_child = AuthService.is_authorised_for_child(id)
    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403
        
    try:
        authorised_child.parent_nickname = new_nickname
        db.session.commit()
        return jsonify({"msg": "Username updated successfully"}), 200
        
    except Exception as e:
        return jsonify({"msg": str(e)}), 400
 




@user_bp.route('/edit_profile_pic/<string:user_type>/<int:id>', methods=['POST'])
@jwt_required()
def edit_profile_pic(user_type, id):
    new_profile_pic = request.json['profile_pic']
    if not new_profile_pic:
        return jsonify({"msg": "No new proflie pic provided"}), 400

    if user_type == "child":
        authorised_child = AuthService.is_authorised_for_child(id)
        if not authorised_child:
            return jsonify({"msg": "Unauthorized access"}), 403
        
        try:
            authorised_child.profile_picture = new_profile_pic
            db.session.commit()
            return jsonify({"msg": "Profile picture updated successfully"}), 200
        
        except Exception as e:

            return jsonify({"msg": str(e)}), 400

    elif user_type == "parent":
        curr_user = get_jwt_identity()
        parent = Parent.query.get(id)
        if parent and parent.email == curr_user['email']:
            try:
                parent.profile_picture = new_profile_pic
                db.session.commit()
                return jsonify({"msg": "Profile picture updated successfully"}), 200
        
            except Exception as e:

                return jsonify({"msg": str(e)}), 400
            
    else:
        return jsonify({"msg": "Invalid user type"}), 400


@user_bp.route('/edit_own_password/<int:id>', methods=['POST'])
@jwt_required()
def edit_own_password(id):
    data = request.json
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    current_user_identification = get_jwt_identity()
    user_email = current_user_identification["email"]
    user_type = current_user_identification['userType']


    if not old_password or not new_password:
        return jsonify({"msg": "Missing old or new password"}), 400

    if user_type == "child":
        child = AuthService.is_authorised_for_child(id)
        if child and bcrypt.check_password_hash(child.password_hash, old_password):
            child.password_hash = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"msg": "Password updated successfully"}), 200
        else:
            return jsonify({"msg": "Invalid old password or user not found"}), 401

    elif user_type == "parent":
        parent = Parent.query.get(id)        
        if parent and parent.email == user_email and bcrypt.check_password_hash(parent.password_hash, old_password):
            parent.password_hash = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"msg": "Password updated successfully"}), 200
        else:
            return jsonify({"msg": "Invalid old password or user not found"}), 401

    else:
        return jsonify({"msg": "Invalid user type"}), 400


@user_bp.route('/edit_child_password/<int:id>', methods=['POST'])
@jwt_required()
def edit_child_password(id):
    data = request.json
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({"msg": "Missing old or new password"}), 400

    child = AuthService.is_authorised_for_child(id)
    if child:
        child.password_hash = bcrypt.generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"msg": "Password updated successfully"}), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403


