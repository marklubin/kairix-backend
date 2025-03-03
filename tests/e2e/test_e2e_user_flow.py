import json
import pytest
from tests.e2e.test_e2e_setup import e2e_app, e2e_client, seed_test_data

def test_complete_user_flow(e2e_client):
    """
    Test a complete user interaction flow:
    1. Create a new user
    2. Create an agent
    3. Start a conversation
    4. Send and receive messages
    5. Verify conversation history
    """
    # Step 1: Create a new user
    user_response = e2e_client.post('/api/users/', json={
        'name': 'Flow Test User',
        'email': 'flow@test.com'
    })
    assert user_response.status_code == 201
    user_data = json.loads(user_response.data)
    user_id = user_data['id']

    # Step 2: Create an agent
    agent_response = e2e_client.post('/api/agents/', json={
        'provider': 'OpenAI',
        'system_prompt': 'You are a helpful assistant',
        'name': 'Flow Test Agent'
    })
    assert agent_response.status_code == 201
    agent_data = json.loads(agent_response.data)
    agent_id = agent_data['id']

    # Step 3: Start a conversation
    conv_response = e2e_client.post('/api/conversations/', json={
        'user_id': user_id,
        'agent_id': agent_id,
        'title': 'Test Conversation'
    })
    assert conv_response.status_code == 201
    conv_data = json.loads(conv_response.data)
    conversation_id = conv_data['id']

    # Step 4: Send a message
    message_response = e2e_client.post('/api/messages/', json={
        'conversation_id': conversation_id,
        'content': 'Hello, this is a test message',
        'role': 'user'
    })
    assert message_response.status_code == 201
    message_data = json.loads(message_response.data)
    assert message_data['content'] == 'Hello, this is a test message'

    # Step 5: Verify conversation history
    history_response = e2e_client.get(f'/api/conversations/{conversation_id}/messages')
    assert history_response.status_code == 200
    history_data = json.loads(history_response.data)
    assert len(history_data) >= 1
    assert any(msg['content'] == 'Hello, this is a test message' for msg in history_data)

def test_user_multiple_conversations(e2e_client, seed_test_data):
    """
    Test user managing multiple conversations:
    1. Use seeded user and agent
    2. Create multiple conversations
    3. Verify conversation listing and access
    """
    user_id = seed_test_data['user_id']
    agent_id = seed_test_data['agent_id']

    # Create multiple conversations
    conversations = []
    for i in range(3):
        conv_response = e2e_client.post('/api/conversations/', json={
            'user_id': user_id,
            'agent_id': agent_id,
            'title': f'Test Conversation {i+1}'
        })
        assert conv_response.status_code == 201
        conv_data = json.loads(conv_response.data)
        conversations.append(conv_data)

    # Verify user's conversation listing
    list_response = e2e_client.get(f'/api/users/{user_id}/conversations')
    assert list_response.status_code == 200
    list_data = json.loads(list_response.data)
    assert len(list_data) == 3

    # Add messages to each conversation
    for conv in conversations:
        message_response = e2e_client.post('/api/messages/', json={
            'conversation_id': conv['id'],
            'content': f'Message in conversation {conv["title"]}',
            'role': 'user'
        })
        assert message_response.status_code == 201

    # Verify messages in each conversation
    for conv in conversations:
        history_response = e2e_client.get(f'/api/conversations/{conv["id"]}/messages')
        assert history_response.status_code == 200
        history_data = json.loads(history_response.data)
        assert len(history_data) >= 1
        assert any(msg['content'] == f'Message in conversation {conv["title"]}' for msg in history_data)
