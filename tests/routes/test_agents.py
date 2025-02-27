import json
from app.models import Agent

def test_create_agent(client):
    """Test creating an agent"""
    response = client.post('/api/agents/', json={
        'provider': 'OpenAI',
        'system_message': 'Hello, world!',
        'settings': {'temperature': 0.7}
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['provider'] == 'OpenAI'
    assert data['system_message'] == 'Hello, world!'
    assert data['settings'] == {'temperature': 0.7}

def test_get_agents(client):
    """Test retrieving all agents"""
    client.post('/api/agents/', json={
        'provider': 'OpenAI',
        'system_message': 'Hello!',
        'settings': {}
    })
    
    response = client.get('/api/agents/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['provider'] == 'OpenAI'

def test_get_agent(client):
    """Test retrieving a single agent by ID"""
    response = client.post('/api/agents/', json={
        'provider': 'Anthropic',
        'system_message': 'Welcome!',
        'settings': {}
    })
    agent_id = json.loads(response.data)['id']
    
    response = client.get(f'/api/agents/{agent_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['provider'] == 'Anthropic'
    assert data['system_message'] == 'Welcome!'

def test_update_agent(client):
    """Test updating an agent"""
    response = client.post('/api/agents/', json={
        'provider': 'Google',
        'system_message': 'Testing...',
        'settings': {}
    })
    agent_id = json.loads(response.data)['id']
    
    response = client.put(f'/api/agents/{agent_id}', json={
        'provider': 'OpenAI',
        'system_message': 'Updated message'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['provider'] == 'OpenAI'
    assert data['system_message'] == 'Updated message'

def test_delete_agent(client):
    """Test deleting an agent"""
    response = client.post('/api/agents/', json={
        'provider': 'DeepMind',
        'system_message': 'AI Agent',
        'settings': {}
    })
    agent_id = json.loads(response.data)['id']
    
    response = client.delete(f'/api/agents/{agent_id}')
    assert response.status_code == 200  # Expecting 200 OK for successful deletion
    
    response = client.get(f'/api/agents/{agent_id}')
    assert response.status_code == 404  # Ensure it's gone