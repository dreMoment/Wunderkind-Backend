from datetime import datetime
from app import db

class Rewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    cost = db.Column(db.Integer, nullable=False, default=10)

    def __init__(self, child_id, title, description, cost):
        self.child_id = child_id
        self.title = title
        self.description = description
        self.cost = cost

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'title': self.title,
            'description': self.description,
            'cost': self.cost
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class PurchasedRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id',ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    cost = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, child_id, title, description, cost):
        self.child_id = child_id
        self.title = title
        self.description = description
        self.cost = cost

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'title': self.title,
            'description': self.description,
            'cost': self.cost,
            'purchase_date': self.purchase_date.isoformat()
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
