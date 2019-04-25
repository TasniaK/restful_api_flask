#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# Array of dictionaries, simpler than using a db for now.
# u for unicode so special characters do not break it.
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Ibuprofen',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# Base path to access this service.
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Get task by user inputted id.
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Shorthand for list comprehension.
    task = [task for task in tasks if task['id'] == task_id]

    # If no id is given.
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# In the case of a 404, return error as JSON data.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Add task with post method.
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # If request is not in JSON format or there is no title.
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        # Get id of last element in tasks, add one.
        'id': tasks[-1]['id'] + 1,
        # Takes user inputted title.
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# Update a task with put method.
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# Delete task with delete method.
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
