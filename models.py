# Task db model
# After any changes to model, flask db migrate to record changes in a new migration script.
# flask db upgrade to import these changes to the db, after reviewing the migration script.
# Migration scripts are source controlled so git commit and push the script.
# If deploying changes to prod env, just merge/pull in changes from dev and then flask db upgrade.
# flask db downgrade can be used to undo the last migration.

from restful_api_app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=True)
    done = db.Column(db.Boolean(create_constraint=False), index=True)

    def __repr__(self):
        return '<Task {}>'.format(self.id)