# app/routes/task_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.routes.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task



task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/get_tasks/<int:child_id>', methods=['GET'])
@jwt_required()
def get_task(child_id):
    authorised_child =AuthService.is_authorised_for_child(child_id)
    if(authorised_child):
        tasks = Task.query.filter_by(child_id = child_id, hide = False).all()
        return jsonify([task.to_dict() for task in tasks]), 200
    else:
        return({"msg" : "unauthorised access"}), 403


@task_bp.route('/get_all_tasks', methods=['GET'])
@jwt_required()
def get_all_tasks():
    tasks = Task.query.filter_by(hide = False).all()
    return jsonify([task.to_dict() for task in tasks]), 200
    

@task_bp.route('/add_task/<int:child_id>', methods=['POST'])
@jwt_required()
def add_task(child_id):
    current_user_identification = get_jwt_identity()

    authorised_child =AuthService.is_authorised_for_child(child_id)
    if(authorised_child):
        try:
            category = request.json['category']
            title = request.json['title']
            description = request.json['description']
            due_date = request.json['due_date']
            daily = request.json['daily']
            weekly = request.json['weekly']
            weekdaily = request.json['weekdaily']
            monthly = request.json['monthly']
            reward = request.json['reward']
            estimated_time = request.json['estimated_time']
        
            user_type = current_user_identification['userType']
            if(user_type == "parent"):
                from_parent = True
            else:
                from_parent = False

            new_task = Task(child_id=child_id, category=category, title=title, description=description, due_date=due_date,daily=daily ,
                        weekly=weekly, weekdaily=weekdaily, monthly=monthly, reward=reward, from_parent=from_parent, estimated_time=estimated_time)
        
            db.session.add(new_task)
            db.session.commit()

            return jsonify({"msg": "Task added successfully", "task": new_task.to_dict()}), 201

        except Exception as e:
            return jsonify({"msg": str(e)}), 400  # Catch and return any error

    else:
        return jsonify({"msg": "Unauthorized access"}), 403
    

@task_bp.route('/edit_task/<int:task_id>', methods=['PUT'])
@jwt_required()
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task:
        authorised_child = AuthService.is_authorised_for_child(task.child_id)
        if authorised_child:
            try:
                data = request.json
                task.update(**data)  # Update task with provided data

                db.session.commit()
                return jsonify({"msg": "Task updated successfully", "task": task.to_dict()}), 200
            except Exception as e:
                return jsonify({"msg": str(e)}), 400
        else:
            return jsonify({"msg": "Unauthorized access"}), 403
    else:
        return jsonify({"msg": "Task not found"}), 404


@task_bp.route('/delete_task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        authorised_child = AuthService.is_authorised_for_child(task.child_id)
        if authorised_child:
            try:
                if task.is_done:
                    # If task is marked as done, set hide to True
                    task.hide = True
                    db.session.commit()
                    return jsonify({"msg": "Task marked as hidden"}), 200
                else:
                    # If task is not done, delete it
                    db.session.delete(task)
                    db.session.commit()
                    return jsonify({"msg": "Task deleted successfully"}), 200
            except Exception as e:
                return jsonify({"msg": str(e)}), 400
        else:
            return jsonify({"msg": "Unauthorized access"}), 403
    else:
        return jsonify({"msg": "Task not found"}), 404


@task_bp.route('/get_task_categories/<int:child_id>', methods=['GET'])
@jwt_required()
def get_task_categories(child_id):

    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        categories = Task.query.with_entities(Task.category).filter_by(child_id=child_id).distinct().all()
        category_list = [category[0] for category in categories if category[0] is not None]
        return jsonify(category_list), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403

    

