# app/routes/child_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.schemas.user_schema import user_schema, users_schema, children_schema
from app.models.parent import Parent
from app.models.child import Child
from app import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes.auth_service import AuthService

child_bp = Blueprint('child_bp', __name__)


@child_bp.route('/get_child/<int:child_id>', methods=['GET'])
@jwt_required()
def get_child(child_id):
    current_user_identification = get_jwt_identity()
    current_user_email = current_user_identification['email']
    user_type = current_user_identification['userType']

    if user_type == "parent":
        parent = Parent.query.filter_by(email=current_user_email).first()
        if parent:
            child = Child.query.filter_by(id=child_id, parent_id = parent.id).first()
            if child:
                return jsonify(child.to_dict())
            else:
                return jsonify({"msg": "Child not found or not authorised"}), 404
        else:

            return jsonify({"msg": "Parent not found"}), 404
    
    elif user_type == "child":    
        parent = Parent.query.filter_by(email=current_user_email).first()
        if parent:
            child = Child.query.filter_by(id=child_id, parent_id=parent.id, username=current_user_identification.get('username')).first()
            if child:
                return jsonify(child.to_dict()), 200
            else:
                return jsonify({"msg": "Unauthorized or child not found"}), 401
        else:
            return jsonify({"msg": "Parent not found"}), 401


    else:
        return jsonify({"msg": "user type is invalid"})        


@child_bp.route('/get_child_point_limit/<int:child_id>', methods=['GET'])
@jwt_required()
def get_child_point_limit(child_id):
    current_user_identification = get_jwt_identity()
    user_type = current_user_identification['userType']
    child = AuthService.is_authorised_for_child(child_id)

    if user_type == "parent" and child:
        point_limit_info = {
            "is_daily_point_limit_enabled": child.is_daily_point_limit_enabled,
            "daily_point_limit": child.daily_point_limit
        }
        return jsonify(point_limit_info)
    else:
        return jsonify({"msg": "Child not found or not authorised"}), 404



@child_bp.route('/update_child_point_limit/<int:child_id>', methods=['POST'])
@jwt_required()
def update_child_point_limit(child_id):
    current_user_identification = get_jwt_identity()
    user_type = current_user_identification['userType']
    child = AuthService.is_authorised_for_child(child_id)

    if user_type == "parent" and child:
        data = request.get_json()

        if 'is_daily_point_limit_enabled' in data:
            child.is_daily_point_limit_enabled = data['is_daily_point_limit_enabled']

        if 'daily_point_limit' in data:
            child.daily_point_limit = data['daily_point_limit'] 

        db.session.commit()

        return jsonify({
            "msg": "point limit updated successfully",
            "is_daily_point_limit_enabled": child.is_daily_point_limit_enabled,
            "daily_point_limit": child.daily_point_limit
        })
    else:
        return jsonify({"msg": "Child not found or not authorised"}), 404
