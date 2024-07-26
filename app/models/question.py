from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_for_parent = db.Column(db.Boolean, nullable=False)
    default = db.Column(db.Boolean, nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id', ondelete='CASCADE'), nullable=True)
    scale = db.Column(db.String(50), nullable=False, default='smiley')




    def __init__(self, text, is_for_parent, scale, default=False, child_id=None):
        self.text = text
        self.scale = scale
        self.is_for_parent = is_for_parent
        self.child_id = child_id
        self.default = default

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_for_parent": self.is_for_parent,
            "default": self.default,
            "child_id": self.child_id,
            "scale": self.scale
        }