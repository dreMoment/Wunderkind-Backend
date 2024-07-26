from flask import Blueprint, request, jsonify
from app import db
from app.routes.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.book import Book

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"msg": "OK"}), 200
    


@book_bp.route('/get_books/<int:child_id>', methods=['GET'])
@jwt_required()
def get_books(child_id):
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        books = Book.query.filter_by(child_id=child_id).all()
        return jsonify([book.to_dict() for book in books]), 200
    else:
        return jsonify({"msg": "Unauthorized access"}), 403


@book_bp.route('/add_book/<int:child_id>', methods=['POST'])
@jwt_required()
def add_book(child_id):

    current_user_identification = get_jwt_identity()
    authorised_child = AuthService.is_authorised_for_child(child_id)
    if authorised_child:
        try:
            title = request.json['title']
            author = request.json['author']
            pages = request.json['pages']
            current_page = request.json['current_page']
            done = request.json['done']
            reward = request.json['reward']
            start_date = request.json.get('start_date', None)
            end_date = request.json.get('end_date', None)


            user_type = current_user_identification['userType']
            if(user_type == "parent"):
                from_parent = True
            else:
                from_parent = False
            
            if(current_page > 0):
                started = True
            else:
                started = False
            
            if(current_page >= pages):
                done = True
            

            new_book = Book(child_id =child_id, title=title, author = author, pages = pages, current_page = current_page, reward = reward, from_parent=from_parent, done=done, started=started, start_date=start_date, end_date=end_date)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"msg": "Book added successfully", "book": new_book.to_dict()}), 201
        except Exception as e:
            return jsonify({"msg": str(e)}), 400
    else:
        return jsonify({"msg": "Unauthorized access"}), 403


@book_bp.route('/edit_book/<int:book_id>', methods=['PUT'])
@jwt_required()
def edit_book(book_id):
    book = Book.query.get(book_id)
    if book:
        authorised_child = AuthService.is_authorised_for_child(book.child_id)
        if authorised_child:
            try:
                data = request.get_json()
                book.update(**data) 
          
                db.session.commit()
                return jsonify({"msg": "Book updated successfully", "book": book.to_dict()}), 200
            except Exception as e:
                print(e)
                return jsonify({"msg": str(e)}), 400
        else:
            return jsonify({"msg": "Unauthorized access"}), 403
    else:
        return jsonify({"msg": "Book not found"}), 404

@book_bp.route('/delete_book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        authorised_child = AuthService.is_authorised_for_child(book.child_id)
        if authorised_child:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"msg": "Book deleted successfully"}), 200
        else:
            return jsonify({"msg": "Unauthorized access"}), 403
    else:
        return jsonify({"msg": "Book not found"}), 404
