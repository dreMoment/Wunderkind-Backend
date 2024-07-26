from app import db 
from datetime import datetime
import pytz


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=True)
    is_from_parent = db.Column(db.Boolean, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id', ondelete='CASCADE')) 
    child_id = db.Column(db.Integer, db.ForeignKey('child.id', ondelete='CASCADE'))  
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))  # Reference the question
    answer_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('Europe/Zurich')))

    def __init__(self, rating, is_from_parent, parent_id=None, child_id=None, question_id=None):
        self.rating = rating
        self.is_from_parent = is_from_parent
        self.parent_id = parent_id
        self.child_id = child_id
        self.question_id = question_id
        self.answer_date = datetime.now(pytz.timezone('Europe/Zurich'))



    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "is_from_parent": self.is_from_parent,
            "parent_id": self.parent_id,
            "child_id": self.child_id,
            "question_id": self.question_id,
            "answer_date": self.answer_date.isoformat() if self.answer_date else None,
        }