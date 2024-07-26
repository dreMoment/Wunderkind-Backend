from flask import Blueprint, jsonify, request
from app import db
from app.models.question import Question
from app.models.child import Child
from app.models.category import Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes.auth_service import AuthService 

category_bp = Blueprint('category_bp', __name__)


# Route to get all cats 
@category_bp.route('/get_categories/<int:id>', methods=['GET'])
@jwt_required()
# can only be done by child
def get_categories(id):

    authorised_child = AuthService.is_authorised_for_child(id)
    if authorised_child:
        categories = Category.query.filter_by(child_id = id).all()
        return jsonify([category.to_dict() for category in categories]), 200

    else:
        return jsonify({"message": "Child not found or not authorised"}), 404
    

# Route to add a cat
@category_bp.route('/add_category/<int:child_id>', methods=['POST'])
@jwt_required()
def add_category(child_id):
    child = AuthService.is_authorised_for_child(child_id)
    if child:
        try:
            name = request.json['name']
            weight = request.json['weight']
            new_cat = Category(child_id=child_id, name = name, color=1, icon="custom", weight=weight)
            db.session.add(new_cat)
            db.session.commit()

            return jsonify({"message": "Category added successfully", "category": new_cat.to_dict()}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Unauthorized access"}), 403
    

# Route to balance cat weights
@category_bp.route('/balance_category_weights/<int:child_id>', methods=['POST'])
@jwt_required()
def balance_category_weights(child_id):
    child = AuthService.is_authorised_for_child(child_id)
    if child:
        try:
            db.session.query(Category).filter_by(child_id=child_id).update({Category.weight: 1/Category.query.filter_by(child_id=child_id).count()})
            db.session.commit()

            return jsonify({"message": "Categories balanced successfully"}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Unauthorized access"}), 403
    

# Route to change weight of one cat
@category_bp.route('/update_category_weight/<int:child_id>/<string:catname>', methods=['POST'])
@jwt_required()
def update_category_weight(child_id, catname):
    child = AuthService.is_authorised_for_child(child_id)
    if child:
        try:
            db.session.query(Category).filter_by(child_id=child_id, catname=catname).update({Category.weight: request.json['weight']})
            db.session.commit()

            return jsonify({"message": "Category weight updated successfully"}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Unauthorized access"}), 403
    

# Route to save all cats
@category_bp.route('/save_weights/<int:child_id>', methods=['POST'])
@jwt_required()
def save_categories(child_id):
    child = AuthService.is_authorised_for_child(child_id)
    if child:
        try:
            for cat in request.json:
                db.session.query(Category).filter_by(child_id=child_id, name=cat['name']).update({Category.weight: cat['weight']})
            db.session.commit()

            return jsonify({"message": "Categories saved successfully"}), 201
        except Exception as e:
            return jsonify({"message": str(e)}), 400
    else:
        return jsonify({"message": "Unauthorized access"}), 403


