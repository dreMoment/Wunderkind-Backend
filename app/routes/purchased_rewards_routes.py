from flask import Blueprint, request, jsonify
from app import db
from app.models.rewards import Rewards
from app.models.rewards import PurchasedRewards
from app.models.child import Child
from app.models.parent import Parent
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.routes.auth_service import AuthService

purchased_reward_bp = Blueprint('purchased_reward_bp', __name__)

@purchased_reward_bp.route('/purchased_rewards/<int:child_id>', methods=['GET'])
@jwt_required()
def get_purchased_rewards(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403

    try:
        purchased_rewards = PurchasedRewards.query.filter_by(child_id=child_id).all()
        return jsonify([reward.to_dict() for reward in purchased_rewards]), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400



@purchased_reward_bp.route('/buy_reward/<int:child_id>', methods=['POST'])
@jwt_required()
def buy_reward(child_id):

    authorised_child = AuthService.is_authorised_for_child(child_id)
    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403

    try:
        title = request.json['title']
        description = request.json['description']
        cost = request.json['cost']
        
            
        bought_reward = PurchasedRewards(child_id = child_id, description = description, title = title, cost = cost)


        if authorised_child.curr_reward < bought_reward.cost:
            return jsonify({"msg": "Insufficient points"}), 400

    
        authorised_child.curr_reward -= bought_reward.cost  # Deduct points
        db.session.commit()  # Commit the points deduction

        db.session.add(bought_reward)
        db.session.commit()
        return jsonify({"msg": "Reward purchased successfully", "purchased_reward": bought_reward.to_dict()}), 201
    
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@purchased_reward_bp.route('/use_reward/<int:purchased_reward_id>', methods=['DELETE'])
@jwt_required()
def use_reward(purchased_reward_id):
    purchased_reward = PurchasedRewards.query.get(purchased_reward_id)
    if(not purchased_reward):
        return jsonify({"msg": "purchased reward not found"}), 404

    authorised_child = AuthService.is_authorised_for_child(purchased_reward.child_id)
    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403

    try:
        db.session.delete(purchased_reward)
        db.session.commit()
        return jsonify({"msg": "Purchased reward deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400