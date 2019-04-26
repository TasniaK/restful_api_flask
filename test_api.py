import json
import base64

# Use client created in conftest to carry out requests.
def test_get_tasks(client):
    response = client.get("/todo/api/v1.0/tasks", headers={"Authorization": "Basic {user}".format(user=base64.b64encode("tasnia:python"))})
    assert response.status_code == 200

def test_get_task(client):
    response = client.get("/todo/api/v1.0/tasks/1", headers={"Authorization": "Basic {user}".format(user=base64.b64encode("tasnia:python"))})
    assert response.status_code == 200

def test_not_found_unauthorized(client):
    response = client.get("/todo/api/v1.0/tasks")
    assert response.status_code == 403

# Only tests one case of returning a 404.
def test_not_found_authorized(client):
    response = client.get("/todo/api/v1.0/tasks/5", headers={"Authorization": "Basic {user}".format(user=base64.b64encode("tasnia:python"))})
    assert response.status_code == 404

def test_create_task(client):
    data = {
        'title': 'Read a book'
    }
    # Headers accepts format [('key', 'value')].
    headers = [
        ('Content-Type', 'application/json'),
        ("Authorization", "Basic {user}".format(user=base64.b64encode("tasnia:python")))
    ]
    response = client.post("/todo/api/v1.0/tasks", json=data, headers=headers)
    assert response.status_code == 201

def test_update_task(client):
    # import pdb;pdb.set_trace()
    data = {
        'done': True
    }
    headers = [
        ('Content-Type', 'application/json'),
        ("Authorization", "Basic {user}".format(user=base64.b64encode("tasnia:python")))
    ]
    response = client.put("/todo/api/v1.0/tasks/2", json=data, headers=headers)
    assert response.status_code == 200

def test_delete_task(client):
    headers = [
        ('Content-Type', 'application/json'),
        ("Authorization", "Basic {user}".format(user=base64.b64encode("tasnia:python")))
    ]
    response = client.delete("/todo/api/v1.0/tasks/3", headers=headers)
    assert response.status_code == 200

def test_unauthorized(client):
    response = client.get("/todo/api/v1.0/tasks", headers={"Authorization": "Basic {user}".format(user=base64.b64encode("tasnia:python"))})
    assert response.status_code == 200