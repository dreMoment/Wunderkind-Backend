from app import db 


class Category(db.Model):
    child_id = db.Column(db.Integer, db.ForeignKey('child.id', ondelete='CASCADE'), primary_key=True)  
    name = db.Column(db.String(255), primary_key=True)
    color = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __init__(self, child_id, name, color, icon, weight=None):
        self.child_id = child_id
        self.name =name
        self.color = color
        self.icon = icon
        self.weight = weight


    def to_dict(self):
        return {
            "cid": self.child_id,
            "name": self.name,
            "color": self.color,
            "icon": self.icon,
            "weight": self.weight
        }