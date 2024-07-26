# app/routes/statistics_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.routes.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.models.answer import Answer
import datetime
import pytz


statistics_bp = Blueprint('statistics_bp', __name__)

@statistics_bp.route('/get_open_task_counts/<int:child_id>', methods=['GET'])
@jwt_required()
def get_open_task_counts(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        categories = Task.query.with_entities(Task.category, db.func.count(Task.id)).filter(Task.child_id == child_id, Task.is_done == False).group_by(Task.category).all()

        open_task_counts = {category: count for category, count in categories if category is not None}
        return jsonify(open_task_counts), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403



def get_time_frame_dates(time_frame):
    swiss_tz = pytz.timezone('Europe/Zurich')
    now = datetime.datetime.now(swiss_tz)

    if time_frame == 'this_week':
        start = now - datetime.timedelta(days=now.weekday())
        end = start + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
    elif time_frame == 'last_week':
        start = now - datetime.timedelta(days=now.weekday() + 7)
        end = start + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
    elif time_frame == 'this_month':
        start = now.replace(day=1)
        end = start.replace(month=start.month % 12 + 1, day=1) - datetime.timedelta(days=1)
    else:  # overall
        start = None
        end = None

    return start, end


@statistics_bp.route('/get_time_spent_categories/<int:child_id>/<string:time_frame>', methods=['GET'])
@jwt_required()
def task_category_stats(child_id, time_frame):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        start_date, end_date = get_time_frame_dates(time_frame)

        # Adjusted query to calculate total time_taken for each category
        query = Task.query.with_entities(
                    Task.category, 
                    db.func.sum(Task.time_taken).label('total_time')
                ).filter(
                    Task.child_id == child_id, 
                    Task.is_done == True
                )

        # Apply time frame filters
        if start_date and end_date:
            query = query.filter(Task.done_date >= start_date, Task.done_date <= end_date)

        # Group by category and execute the query

        categories = query.group_by(Task.category).all()

        # Create a dictionary from the query results
        category_stats = {category: float(total_time) for category, total_time in categories if category is not None}
        return jsonify(category_stats), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403


@statistics_bp.route('/get_child_answers/<int:child_id>/<int:question_id>/<string:time_frame>', methods=['GET'])
@jwt_required()
def get_child_answers(child_id, question_id, time_frame):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        start_date, end_date = get_time_frame_dates(time_frame)

        # Use filter_by for simpler queries
        query = Answer.query.filter_by(
                    child_id=child_id,
                    question_id=question_id
                )

        # Apply time frame filters with filter, as filter_by cannot handle greater/lesser than operations
        if start_date and end_date:
            query = query.filter(Answer.answer_date >= start_date, Answer.answer_date <= end_date)

        # Execute the query
        answers = query.all()

        if answers:
            # Assuming you have a to_dict method in your Answer model to serialize the object
            answers_list = [answer.to_dict() for answer in answers]
            return jsonify({"answers": answers_list}), 200
        else:
            return jsonify({"message": "No answers found"}), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403
