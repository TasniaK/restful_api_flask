#! /bin/python

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pdb

app = Flask(__name__)

app.config.from_object(Config)

# Represents the db as an object.
db = SQLAlchemy(app)
# Represents the migration engine as an object.
migrate = Migrate(app, db)

from models import Task

# Array of dictionaries, simpler than using a db for now.
# u for unicode so special characters do not break it.

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Ibuprofen',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'tasnia':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

def validate_auth():
    auth = request.authorization
    if not auth:
        return False
    return True

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
# @auth.login_required
def get_tasks():
    tasks = Task.query.all()
    task_info_list = []
    # pdb.set_trace()
    for task in tasks:
        task_info = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'done': task.done
        }
        task_info_list.append(task_info)
    if not validate_auth():
        return jsonify({'tasks': [make_public_task(task_info) for task_info in task_info_list]})
    return jsonify({'tasks': [task_info_list]})
    # return jsonify({'tasks': [make_public_task(task) for task in tasks]})


# Get task by user inputted id.
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
#@auth.login_required
def get_task(task_id):
    # Shorthand for list comprehension.
    task_object = Task.query.get_or_404(task_id)
    if task_id == task_object.id:
        task = [{
            'id': task_id,
            'title': task_object.title,
            'description': task_object.description,
            'done': task_object.done
        }]
    # If no task is found.
    # if task_id == 0:
    #     abort(404)
    return jsonify({'task': task[0]})


# In the case of a 404, return error as JSON data.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Add task with post method.
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():

    # If request is not in JSON format or there is no title.
    if not request.json or not 'title' in request.json:
        abort(400)

    title = request.json['title']
    description = request.json.get('description', "")
    done = False

    task_object = Task(title = title, description = description, done = done)
    db.session.add(task_object)
    db.session.commit()
    task_id = task_object.id
    return jsonify({'task': {'id': task_id, 'title': title, 'description': description, 'done': done}}), 201


# Update a task with put method.
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):

    original_task = Task.query.filter_by(id=task_id).first()

    if task_id == 0 or not original_task:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json:
        if type(request.json['title']) is not unicode:
            abort(400)
        else:
            original_task.title = request.json['title']
    if 'description' in request.json:
        if type(request.json['description']) is not unicode:
            abort(400)
        else:
            original_task.description = request.json['description']

    if 'done' in request.json:
        if type(request.json['done']) is not bool:
            abort(400)
        else:
            original_task.done = request.json['done']

    db.session.commit()


    return jsonify({'task': str(original_task)})


# Delete task with delete method.
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    """

    :param task_id:
    :return:
    """
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


# For clients, instead of task id, return public uri of task.
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for(
                'get_task', task_id=task['id'], _external=True
            )
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True)
