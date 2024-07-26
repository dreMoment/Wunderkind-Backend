from flask import Blueprint, request, jsonify
from app import db
from app.models.rewards import Rewards
from app.models.child import Child
from app.models.parent import Parent
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.routes.auth_service import AuthService

reward_bp = Blueprint('reward_bp', __name__)



@reward_bp.route('/get_rewards/<int:child_id>', methods=['GET'])
@jwt_required()
def get_rewards(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403

    try:
        purchased_rewards = Rewards.query.filter_by(child_id=child_id).all()
        return jsonify([reward.to_dict() for reward in purchased_rewards]), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@reward_bp.route('/add_reward/<int:child_id>', methods=['POST'])
@jwt_required()
def add_task(child_id):

    
    child_id_sent = request.json['child_id']
    if (child_id_sent != child_id):
        return jsonify({"msg": "child_ids don't match"}), 403

    authorised_child = AuthService.is_authorised_for_child(child_id)
    if(authorised_child):
        try:
            title = request.json['title']
            description = request.json['description']
            cost = request.json['cost']

            
            new_reward = Rewards(child_id = child_id, description = description, title = title, cost = cost)
            db.session.add(new_reward)
            db.session.commit()

            return jsonify({"msg": "Reward added successfully", "task": new_reward.to_dict()}), 201

        except Exception as e:
            return jsonify({"msg": str(e)}), 400  # Catch and return any error

    else:
        return jsonify({"msg": "Unauthorized access"}), 403
    



@reward_bp.route('/edit_reward/<int:reward_id>', methods=['PUT'])
@jwt_required()
def edit_reward(reward_id):
    reward = Rewards.query.get(reward_id)
    
    if not reward:
        return jsonify({"msg": "Reward not found"}), 404

    authorised_child = AuthService.is_authorised_for_child(reward.child_id)

    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403

    try:
        data = request.json
        reward.update(**data)
        db.session.commit()
        return jsonify({"msg": "Reward updated successfully", "reward": reward.to_dict()}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@reward_bp.route('/delete_reward/<int:reward_id>', methods=['DELETE'])
@jwt_required()
def delete_reward(reward_id):
    reward = Rewards.query.get(reward_id)
    if not reward:
        return jsonify({"msg": "Reward not found"}), 404

    authorised_child = AuthService.is_authorised_for_child(reward.child_id)
    if not authorised_child:
        return jsonify({"msg": "Unauthorized access"}), 403


    try:
        db.session.delete(reward)
        db.session.commit()
        return jsonify({"msg": "Reward deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

