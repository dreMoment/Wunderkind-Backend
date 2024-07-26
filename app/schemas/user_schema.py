# app/schemas/user_schema.py
from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ChildSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'username', 'parent_nickname', 'parent_id')

child_schema = ChildSchema()
children_schema = ChildSchema(many=True)