# app/routes/parent_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.schemas.user_schema import user_schema, users_schema, children_schema
from app.models.parent import Parent
from app.models.child import Child
from app.routes.auth_service import AuthService
from app import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity


parent_bp = Blueprint('parent_bp', __name__)


@parent_bp.route('/get_children/<int:parent_id>', methods=['GET'])
@jwt_required()
def get_children(parent_id):
    current_user_identification = get_jwt_identity()
    current_user_email = current_user_identification['email']
    parent = Parent.query.filter_by(email = current_user_email).first()

    if parent and parent.id == parent_id:
        children = Child.query.filter_by(parent_id = parent_id).all()
        children_data = [child.to_dict() for child in children]
        return jsonify(children_data), 200
    else:
        return jsonify({"msg": "Unauthorized or parent not found"}), 401
 

@parent_bp.route('/delete_account/<int:user_id>/<user_type>', methods=['POST'])
@jwt_required()
def delete_account(user_id, user_type):
    data = request.json  
    password = data.get("password")
    current_user_identification = get_jwt_identity()
    current_user_email = current_user_identification['email']
    
    if not AuthService.authenticate_parent(current_user_email, password):
        return jsonify({"msg": "Invalid password"}), 403

    if user_type == "child":
        child = AuthService.is_authorised_for_child(user_id)
        if child:
            db.session.delete(child)
            db.session.commit()
            return jsonify({"msg": "Child deleted successfully"}), 200
        else:
            return jsonify({"msg": "Child not found or not authorized"}), 404
    
    if user_type == "parent":

        parent = Parent.query.filter_by(email = current_user_email).first()
        if parent and parent.id == user_id:
            db.session.delete(parent)
            db.session.commit()
            return jsonify({"msg": "Parent deleted successfully"}), 200
        
        else:
            return jsonify({"msg": "Parent not found or not authorized"}), 404

    else:
        return jsonify({"msg": "Invalid user type"}), 401