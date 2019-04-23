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
@app.route('/todo/api/v1.0/tasks', methods=['GET'])

# Flask's jsonify function returns above task data as JSON data.
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)