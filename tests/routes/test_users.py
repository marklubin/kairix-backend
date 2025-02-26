import json
from app.models import User

def test_create_user(client):
    response = client.post('/api/users/', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'

def test_get_users(client):
    # Create test user
    client.post('/api/users/', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    
    response = client.get('/api/users/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test User'

def test_get_user(client):
    # Create test user
    response = client.post('/api/users/', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    user_id = json.loads(response.data)['id']
    
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test User'

def test_update_user(client):
    # Create test user
    response = client.post('/api/users/', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    user_id = json.loads(response.data)['id']
    
    response = client.put(f'/api/users/{user_id}', json={
        'name': 'Updated User'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated User'

def test_delete_user(client):
    # Create test user
    response = client.post('/api/users/', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    user_id = json.loads(response.data)['id']
    
    response = client.delete(f'/api/users/{user_id}')
    assert response.status_code == 204
    
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 404