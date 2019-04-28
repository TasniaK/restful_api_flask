# Task db model

from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=True)
    done = db.Column(db.Boolean(create_constraint=False), index=True)

    def __repr__(self):
        return '<Task {}>'.format(self.id)