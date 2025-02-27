import json

def test_create_message(client):
    """Test creating a message"""
    conversation = client.post('/api/conversations/', json={
        'user_id': 'test-user',
        'agent_id': 'test-agent'
    })
    conversation_id = json.loads(conversation.data)['id']

    response = client.post('/api/messages/', json={
        'conversation_id': conversation_id,
        'role': 'user',
        'content': 'Hello!'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['role'] == 'user'
    assert data['content'] == 'Hello!'