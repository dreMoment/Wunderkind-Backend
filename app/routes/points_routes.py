from flask import Blueprint, request, jsonify
from app import db
from app.models.question import Question
from app.models.answer import Answer
from app.models.child import Child
from app.models.parent import Parent
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.routes.auth_service import AuthService
import pytz


points_bp = Blueprint('points_bp', __name__)

@points_bp.route('/get_current_points/<int:child_id>', methods=['GET'])
@jwt_required()
def get_current_rewards(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        reward = authorised_child.curr_reward
        return jsonify({"reward": reward}), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403


@points_bp.route('/get_total_points/<int:child_id>', methods=['GET'])
@jwt_required()
def get_total_rewards(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        reward = authorised_child.tot_reward
        return jsonify({"reward": reward}), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403


@points_bp.route('/add_points/<int:child_id>', methods=['PUT'])
@jwt_required()
def add_reward(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    current_user_identification = get_jwt_identity()
    user_type = current_user_identification['userType']


    if authorised_child:
        try:
            data = request.get_json()
            amount = data.get('amount')
            overwrite = data.get('overwrite', False)

            if amount is None or not isinstance(amount, int):
                return jsonify({"msg": "Invalid amount"}), 400
            
            if user_type == "child" and not overwrite:
                authorised_child.daily_points_earned += amount


            authorised_child.curr_reward += amount
            authorised_child.tot_reward += amount
            db.session.commit()

            return jsonify({"msg": "Reward updated successfully", "curr_reward": authorised_child.curr_reward, "tot_reward": authorised_child.tot_reward}), 200
        
        except Exception as e:
            return jsonify({"msg": "An error occurred"}), 500
    else:
        return jsonify({"msg": "Unauthorized access"}), 403
    

@points_bp.route('/use_points/<int:child_id>', methods=['PUT'])
@jwt_required()
def use_reward(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        try:
            data = request.get_json()
            amount = data.get('amount')
            if amount is None or not isinstance(amount, int) and (authorised_child.curr_reward - amount >= 0):
                return jsonify({"msg": "Invalid amount"}), 400

            authorised_child.curr_reward -= amount
            db.session.commit()

            return jsonify({"msg": "Reward updated successfully", "curr_reward": authorised_child.curr_reward}), 200
        
        except Exception as e:
            return jsonify({"msg": "An error occurred"}), 500
    else:
        return jsonify({"msg": "Unauthorized access"}), 403
    

@points_bp.route('/check_point_limit/<int:child_id>/<int:amount>', methods=['GET'])
@jwt_required()
def check_point_limit(child_id, amount):
    child = AuthService.is_authorised_for_child(child_id)
    if child and child.is_daily_point_limit_enabled:
        # Get current Swiss time
        swiss_timezone = pytz.timezone('Europe/Zurich')
        current_swiss_time = datetime.now(swiss_timezone)

        # Reset daily rewards if it's a new day
        if child.last_point_claim_date == None or child.last_point_claim_date.date() != current_swiss_time.date():
            child.daily_points_earned = 0
            child.last_point_claim_date = current_swiss_time

        if child.daily_points_earned + amount > child.daily_point_limit:
            return jsonify({"result": False}), 200  # Return False as JSON response
        
        return jsonify({"result": True}), 200  # Return False as JSON response

    
    return jsonify({"result": True}), 200  # Return False as JSON response

        
            

