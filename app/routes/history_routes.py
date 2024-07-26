from flask import Blueprint, request, jsonify
from app.models.task import Task
from app import db
from app.routes.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date

history_bp = Blueprint('history_bp', __name__)

@history_bp.route('/get_data/<int:child_id>', methods=['GET'])
@jwt_required()
def get_data(child_id):
    # Get screentime, activitytime, readingtime for a child for today
    current_user_identification = get_jwt_identity()

    authorised_child =AuthService.is_authorised_for_child(child_id)
    if(authorised_child):
        try:
            tasks = Task.query.filter_by(child_id = child_id, category="sport & outdoor").all()

            pa_time = 0.0
            for task in tasks:
                if task.done_date == date.today():
                    pa_time+=task.time_taken/60

            screen_time = 0.0
            tasks = Task.query.filter_by(child_id = child_id, category="spass am bildschirm").all()
            for task in tasks:
                if task.done_date == date.today():
                    screen_time+=task.time_taken/60
            
            reading_time = 0.0
            tasks = Task.query.filter_by(child_id = child_id, category="lesen").all()
            for task in tasks:
                if task.done_date == date.today():
                    reading_time+=task.time_taken/60


            #print("Physical Activity Time: ", pa_time)
            #print("Screen Time: ", screen_time)
            #print("Reading Time: ", reading_time)
            return jsonify({"msg": "History Entry for today found", "entry": {"physical_activity":pa_time, "screen_time":screen_time, "reading_time":reading_time}}), 201

        except Exception as e:
            return jsonify({"msg": str(e)}), 400  # Catch and return any error

    else:
        return jsonify({"msg": "Unauthorized access"}), 403

@history_bp.route('/get_data_for_date/<int:child_id>/<string:selected_date>', methods=['GET'])
@jwt_required()
def get_data_for_date(child_id, selected_date):

    selected_date = datetime.strptime(selected_date[:10], '%Y-%m-%d').date()
    
    # Get screentime, activitytime, readingtime for a child for today
    current_user_identification = get_jwt_identity()

    authorised_child =AuthService.is_authorised_for_child(child_id)
    if(authorised_child):
        try:
            tasks = Task.query.filter_by(child_id = child_id, category="sport & outdoor").all()

            pa_time = 0.0
            for task in tasks:
                if task.done_date == selected_date:
                    pa_time+=task.time_taken/60

            screen_time = 0.0
            tasks = Task.query.filter_by(child_id = child_id, category="spass am bildschirm").all()
            for task in tasks:
                if task.done_date == selected_date:
                    screen_time+=task.time_taken/60
            
            reading_time = 0.0
            tasks = Task.query.filter_by(child_id = child_id, category="lesen").all()
            for task in tasks:
                if task.done_date == selected_date:
                    reading_time+=task.time_taken/60


            #print("Physical Activity Time: ", pa_time)
            #print("Screen Time: ", screen_time)
            #print("Reading Time: ", reading_time)
            return jsonify({"msg": "History Entry for today found", "entry": {"physical_activity":pa_time, "screen_time":screen_time, "reading_time":reading_time}}), 201

        except Exception as e:
            return jsonify({"msg": str(e)}), 400  # Catch and return any error

    else:
        return jsonify({"msg": "Unauthorized access"}), 403

