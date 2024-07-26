from app import db
from flask_login import UserMixin
from app.models.parent import Parent
from app.models.question import Question
from datetime import datetime


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(300))
    parent_nickname = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id', ondelete='CASCADE'), nullable=False)
    profile_picture = db.Column(db.String(255))
    curr_reward = db.Column(db.Integer, default=0)
    tot_reward = db.Column(db.Integer, default=0)
    is_daily_point_limit_enabled = db.Column(db.Boolean, default=False)
    daily_point_limit = db.Column(db.Integer, default=0)
    daily_points_earned = db.Column(db.Integer, default=0)
    last_point_claim_date = db.Column(db.DateTime, nullable=True)
    show_tutorial = db.Column(db.Boolean, nullable=False, default=True)
    child_type = db.Column(db.Integer, nullable=False, default=0)
    #child_type = 0: normal child, 1: sports cannon, 2: book worm



    __table_args__ = (db.UniqueConstraint('username', 'parent_id', name='_parent_username_uc'),)

    def __init__(self, username, password_hash, parent_nickname, parent_id, profile_picture):
        self.username = username
        self.password_hash = password_hash
        self.parent_nickname = parent_nickname
        self.parent_id = parent_id
        self.profile_picture = profile_picture
        self.is_daily_point_limit_enabled = False
        self.daily_point_limit = 0
        self.daily_points_earned = 0
        self.show_tutorial = True

        

    def get_parent_email(self):
        parent = Parent.query.get(self.parent_id)
        return parent.email 
    
    def to_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "parent_nickname": self.parent_nickname,
            "parent_id":self.parent_id,
            "profile_picture": self.profile_picture,
            "curr_reward": self.curr_reward,
            "tot_reward" : self.tot_reward,
            "is_daily_reward_limit_enabled" : self.is_daily_point_limit_enabled,
            "daily_point_limit" : self.daily_point_limit,
            "daily_points_earned" : self.daily_points_earned,
            "last_point_claim_date": self.last_point_claim_date,
            "child_type": self.child_type

        }
    
