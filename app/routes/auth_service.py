from app import db, bcrypt, login_manager
from app.models.parent import Parent
from app.models.child import Child
from flask_jwt_extended import jwt_required, get_jwt_identity



class AuthService:
    @staticmethod
    def authenticate_parent(email, password):
        user = Parent.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return True
        return False

    @staticmethod
    def authenticate_child(email, username, password):
        parent = Parent.query.filter_by(email=email).first()
        if parent:
            child = Child.query.filter_by(parent_id=parent.id, username=username).first()
            if child and bcrypt.check_password_hash(child.password_hash, password):
                return True
        return False
    

    @staticmethod
    def is_authorised_for_child(child_id):
        current_user_identification = get_jwt_identity()
        current_user_email = current_user_identification['email']
        user_type = current_user_identification['userType']

        if user_type == "child":
            username = current_user_identification['username']
            parent = Parent.query.filter_by(email=current_user_email).first()
            if parent:
                child = Child.query.filter_by(parent_id=parent.id, username=username).first()
                if child and child.id == child_id:
                    return child
                else:
                    return None
            
        elif user_type == "parent":
            parent = Parent.query.filter_by(email=current_user_email).first()
            if parent:
                child = Child.query.filter_by(id=child_id, parent_id=parent.id).first()
                if child:
                    return child
                else:
                    return None
            else:
                return None

        else:
            return None



