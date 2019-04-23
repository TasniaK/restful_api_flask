#!flask/bin/python
from flask import Flask, jsonify

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
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Shorthand for list comprehension.
    task = [task for task in tasks if task['id'] == task_id]

    # If no id is given.
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run(debug=True)