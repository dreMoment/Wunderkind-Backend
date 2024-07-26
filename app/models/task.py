from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    due_date= db.Column(db.Date, nullable=False)
    done_date = db.Column(db.Date, nullable=True)
    estimated_time = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=True)
    daily = db.Column(db.Boolean, default=False)
    weekly = db.Column(db.Boolean, default=False)
    weekdaily = db.Column(db.Boolean, default=False)
    monthly = db.Column(db.Boolean, default=False)
    is_done = db.Column(db.Boolean, default=False)
    reward = db.Column(db.Integer, nullable=True, default=10)
    from_parent = db.Column(db.Boolean, nullable=False, default=False)
    hide = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, child_id, category, title, due_date, estimated_time, description=None, daily=False, weekly=False, weekdaily=False, monthly=False, reward = 10, from_parent=False, hide=False):
        self.child_id = child_id
        self.category = category
        self.title = title
        self.description = description
        self.due_date = due_date
        self.daily = daily
        self.weekly = weekly
        self.weekdaily = weekdaily
        self.monthly = monthly
        self.reward = reward
        self.from_parent = from_parent
        self.hide = hide
        self.estimated_time = estimated_time


    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "done_date": self.done_date.isoformat() if self.done_date else None,
            "daily": self.daily,
            "weekly": self.weekly,
            "weekdaily": self.weekdaily,
            "monthly": self.monthly,
            "is_done": self.is_done,
            "estimated_time": self.estimated_time,
            "time_taken": self.time_taken,
            "reward" : self.reward,
            "from_parent": self.from_parent,
            "hide" : self.hide
    }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
