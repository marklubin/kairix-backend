import json

def test_create_conversation(client):
    """Test creating a conversation"""
    response = client.post('/api/conversations/', json={
        'user_id': 'test-user',
        'agent_id': 'test-agent'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user_id'] == 'test-user'
    assert data['agent_id'] == 'test-agent'

def test_get_conversations(client):
    """Test retrieving all conversations"""
    response = client.get('/api/conversations/')
    assert response.status_code == 200