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

question_bp = Blueprint('question_bp', __name__)


# Route to get all questions depending on whfether the user is a parent or child
@question_bp.route('/get_questions/<user_type>/<int:id>', methods=['GET'])
@jwt_required()
def get_questions(user_type, id):
    curr_user = get_jwt_identity()

    if user_type == 'parent':
        parent = Parent.query.get(id)
        if parent and parent.email == curr_user['email']:
            questions = Question.query.filter_by(is_for_parent=True).all()
            return jsonify({'questions': [question.to_dict() for question in questions]}), 200
        else:
            return jsonify({"message": "Parent not found"}), 404
        
    elif user_type == 'child':
        child = Child.query.get(id)
        child2 = AuthService.is_authorised_for_child(id)
        if child and child2:
            default_questions = Question.query.filter_by(is_for_parent=False, default = True).all()
            questions = Question.query.filter_by(child_id = child.id).all()
            all_questions = default_questions + questions
            return jsonify({'questions': [question.to_dict() for question in all_questions]}), 200

        else:
            return jsonify({"message": "Child not found or not authorised"}), 404
  

    else:
        return jsonify({"msg": "Invalid user type"}), 400




# Route to add a question (for parents to add questions)
@question_bp.route('/add_question/<int:child_id>', methods=['POST'])
@jwt_required()
def add_question(child_id):
    child = AuthService.is_authorised_for_child(child_id)
    if child:
        try:
            text = request.json['text']
            scale = request.json.get('scale', 'smiley')
            new_question = Question(text=text, is_for_parent=False,scale=scale, child_id=child_id)
            db.session.add(new_question)
            db.session.commit()

            return jsonify({"message": "Question added successfully", "question": new_question.to_dict()}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Unauthorized access"}), 403



# Route to delete non-default questions (for parents)
@question_bp.route('/delete_question/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    user_type = get_jwt_identity().get('userType')

    if user_type == 'parent':
        question = Question.query.get(question_id)

        if question:
            if not question.default:
                db.session.delete(question)
                db.session.commit()
                return jsonify({"message": "Question deleted successfully"}), 200
            else:
                return jsonify({"message": "Cannot delete a default question"}), 400
        else:
            return jsonify({"message": "Question not found"}), 404
    else:
        return jsonify({"message": "Unauthorized access"}), 403


# Route to check if a question has been answered today. Todo, see if child or parent
@question_bp.route('/check_answered/<string:user_type>/<int:question_id>/<int:user_id>', methods=['GET'])
@jwt_required()
def check_answered(user_type, question_id, user_id):
    curr_user = get_jwt_identity()
    utc_now = datetime.utcnow()
    swiss_tz = pytz.timezone('Europe/Zurich')
    swiss_now = utc_now.replace(tzinfo=pytz.utc).astimezone(swiss_tz).date()


    if user_type == 'parent':
        parent = Parent.query.get(user_id)
        if parent and parent.email == curr_user['email']:

            # Check if the question has been answered by the user today
            answered = Answer.query.filter_by(question_id=question_id, parent_id=user_id)
            answered = answered.filter(db.func.DATE(Answer.answer_date) == swiss_now).first()
            if answered:
                return jsonify({"message": "Question already answered", "answer": answered.answer_text}), 200
            else:
                return jsonify({"message": "Question not answered yet"}), 200
        
        else:
            return jsonify({"message": "Unauthorized access or parent not found"}), 403

    elif user_type == 'child':
        child = AuthService.is_authorised_for_child(user_id)
        if child:
            answered = Answer.query.filter_by(question_id=question_id, child_id=user_id)
            answered = answered.filter(db.func.DATE(Answer.answer_date) == swiss_now).first()
            if answered:
                return jsonify({"message": "Question already answered", "answer": answered.answer_text}), 200
            else:
                return jsonify({"message": "Question not answered yet"}), 200
        
        else:
            return jsonify({"message": "Unauthorized access or child not found"}), 403


    else:
        return jsonify({"message": "Invalid user type"}), 400

# Get unanswered questions
@question_bp.route('/get_unanswered_questions/<int:child_id>', methods=['GET'])
@jwt_required()
def get_unanswered_questions(child_id):

    curr_user = get_jwt_identity()
    user_type = get_jwt_identity().get('userType')
    utc_now = datetime.utcnow()
    swiss_tz = pytz.timezone('Europe/Zurich')
    swiss_now = utc_now.replace(tzinfo=pytz.utc).astimezone(swiss_tz).date()

    if user_type == 'parent':
        parent_id = Child.query.get(child_id).parent_id
        parent = Parent.query.get(parent_id)
        if parent and parent.email == curr_user['email']:
            questions = Question.query.filter_by(is_for_parent=True).all()
            unanswered_questions = []
            for question in questions:
                answered_today = Answer.query.filter_by(question_id=question.id, child_id=child_id).filter(db.func.DATE(Answer.answer_date) == swiss_now).first()
                if not answered_today:
                    unanswered_questions.append(question)
            return jsonify({'questions': [q.to_dict() for q in unanswered_questions]}), 200
        else:
            return jsonify({"message": "Parent not found"}), 404

    elif user_type == 'child':
        child = AuthService.is_authorised_for_child(child_id)
        if child :
            default_questions = Question.query.filter_by(is_for_parent=False, default = True).all()
            child_questions = Question.query.filter_by(child_id=child.id).all()
            all_questions = Question.query.all()
            all_questions = default_questions + child_questions
            unanswered_questions = []
            for question in all_questions:
                answered_today = Answer.query.filter_by(question_id=question.id, child_id=child_id).filter(db.func.DATE(Answer.answer_date) == swiss_now).first()
                if not answered_today:
                    unanswered_questions.append(question)
            return jsonify({'questions': [q.to_dict() for q in unanswered_questions]}), 200

        else:
            return jsonify({"message": "Child not found or not authorised"}), 404

    else:
        return jsonify({"msg": "Invalid user type"}), 400

# Route to submit an answer to a question, also send user's id
@question_bp.route('/submit_answer', methods=['POST'])
@jwt_required()
def submit_answer():
    try:
        rating = request.json['rating']
        is_from_parent = request.json['is_from_parent'] 
        parent_id = request.json['parent_id']
        child_id = request.json['child_id']
        question_id = request.json['question_id']
        new_answer = Answer(rating=rating, is_from_parent=is_from_parent, parent_id=parent_id,child_id=child_id, question_id=question_id)
        db.session.add(new_answer)
        db.session.commit()

        return jsonify({"message": "Answer submitted successfully", "answer": new_answer.to_dict()}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# Route to view the answer to a specific question
@question_bp.route('/get_answers/<string:user_type>/<int:question_id>/<int:user_id>', methods=['GET'])
@jwt_required()
def view_answer(user_type, question_id, user_id):
    curr_user = get_jwt_identity()
    answers = None  # Initialize answers

    if user_type == 'parent':
        parent = Parent.query.get(user_id)
        if parent and parent.email == curr_user['email']:
            answers = Answer.query.filter_by(question_id=question_id, parent_id=user_id).all()


    elif user_type == 'child':
        child = AuthService.is_authorised_for_child(user_id)
        if child:
            answers = Answer.query.filter_by(question_id=question_id, child_id=user_id).all()

    else:     
        return jsonify({"message": "Invalid user type"}), 401

    if answers:
        # Assuming you have a to_dict method in your Answer model to serialize the object
        answers_list = [answer.to_dict() for answer in answers]
        return jsonify({"answers": answers_list}), 200
    else:
        return jsonify({"message": "No answers found"}), 200

@question_bp.route('/get_all_answers/<string:user_type>', methods=['GET'])
@jwt_required()
def get_all_answers(user_type):
    curr_user = get_jwt_identity()
    answers = None  # Initialize answers

    if user_type == 'parent':
            answers = Answer.query.filter_by(is_from_parent=True).all()


    elif user_type == 'child':
            answers = Answer.query.filter_by(is_from_parent=False).all()

    else:     
        return jsonify({"message": "Invalid user type"}), 401
    
    print(answers)

    # Assuming you have a to_dict method in your Answer model to serialize the object
    answers_list = [answer.to_dict() for answer in answers]
    return jsonify({"answers": answers_list}), 200

@question_bp.route('/get_all_happiness_answers/<string:user_type>', methods=['GET'])
@jwt_required()
def get_all_happiness_answers(user_type):
    curr_user = get_jwt_identity()
    answers = None  # Initialize answers

    if user_type == 'parent':
            answers = Answer.query.filter_by(is_from_parent=True).all()


    elif user_type == 'child':
            answers = Answer.query.filter_by(is_from_parent=False).all()

    else:     
        return jsonify({"message": "Invalid user type"}), 401
    
    print(answers)

    # Assuming you have a to_dict method in your Answer model to serialize the object
    answers_list = [answer.to_dict() for answer in answers]
    answers_list.where(answers_list['question_id'] == 1)
    return jsonify({"answers": answers_list}), 200