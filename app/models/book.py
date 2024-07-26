from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    started = db.Column(db.Boolean, default=False, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    current_page = db.Column(db.Integer, default=0, nullable=True)
    start_date =db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    reward = db.Column(db.Integer, nullable=False, default = 10)
    from_parent = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'title': self.title,
            'author': self.author,
            'pages': self.pages,
            'started': self.started,
            'done': self.done,
            'current_page': self.current_page,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'reward' : self.reward,
            'from_parent' : self.from_parent
        }


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)