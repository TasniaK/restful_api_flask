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

if __name__ == '__main__':
    app.run(debug=True)
