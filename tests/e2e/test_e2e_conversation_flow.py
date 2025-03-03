import json
import pytest
from tests.e2e.test_e2e_setup import e2e_app, e2e_client, seed_test_data

def test_conversation_with_context(e2e_client, seed_test_data):
    """
    Test a conversation flow with context maintenance:
    1. Start conversation with context
    2. Send multiple related messages
    3. Verify context preservation
    """
    user_id = seed_test_data['user_id']
    agent_id = seed_test_data['agent_id']

    # Create conversation with initial context
    conv_response = e2e_client.post('/api/conversations/', json={
        'user_id': user_id,
        'agent_id': agent_id,
        'title': 'Context Test Conversation',
        'context': 'This is a technical discussion about Python'
    })
    assert conv_response.status_code == 201
    conv_data = json.loads(conv_response.data)
    conversation_id = conv_data['id']

    # Send series of related messages
    messages = [
        'What are the key features of Python?',
        'How does Python handle memory management?',
        'Can you explain garbage collection in Python?'
    ]

    for msg in messages:
        message_response = e2e_client.post('/api/messages/', json={
            'conversation_id': conversation_id,
            'content': msg,
            'role': 'user'
        })
        assert message_response.status_code == 201

    # Verify conversation history and context
    history_response = e2e_client.get(f'/api/conversations/{conversation_id}/messages')
    assert history_response.status_code == 200
    history_data = json.loads(history_response.data)
    assert len(history_data) >= len(messages)
    
    # Verify messages are in correct order
    user_messages = [msg for msg in history_data if msg['role'] == 'user']
    for i, msg in enumerate(messages):
        assert user_messages[i]['content'] == msg

def test_multi_agent_conversation(e2e_client, seed_test_data):
    """
    Test conversation involving multiple agents:
    1. Create multiple agents
    2. Start conversations with different agents
    3. Compare responses and interactions
    """
    user_id = seed_test_data['user_id']

    # Create additional test agents
    agents = []
    for i in range(2):
        agent_response = e2e_client.post('/api/agents/', json={
            'provider': 'OpenAI',
            'system_prompt': f'You are assistant {i+1} specialized in Python',
            'name': f'Test Agent {i+1}'
        })
        assert agent_response.status_code == 201
        agents.append(json.loads(agent_response.data))

    # Create conversations with each agent
    conversations = []
    for agent in agents:
        conv_response = e2e_client.post('/api/conversations/', json={
            'user_id': user_id,
            'agent_id': agent['id'],
            'title': f'Conversation with {agent["name"]}'
        })
        assert conv_response.status_code == 201
        conversations.append(json.loads(conv_response.data))

    # Send same message to all agents
    test_message = 'What is your specialization?'
    for conv in conversations:
        message_response = e2e_client.post('/api/messages/', json={
            'conversation_id': conv['id'],
            'content': test_message,
            'role': 'user'
        })
        assert message_response.status_code == 201

    # Verify responses from each agent
    for conv in conversations:
        history_response = e2e_client.get(f'/api/conversations/{conv["id"]}/messages')
        assert history_response.status_code == 200
        history_data = json.loads(history_response.data)
        assert len(history_data) >= 2  # At least user message and agent response

def test_conversation_management(e2e_client, seed_test_data):
    """
    Test conversation management features:
    1. Create conversation
    2. Update conversation title
    3. Archive conversation
    4. Retrieve archived conversations
    """
    user_id = seed_test_data['user_id']
    agent_id = seed_test_data['agent_id']

    # Create new conversation
    conv_response = e2e_client.post('/api/conversations/', json={
        'user_id': user_id,
        'agent_id': agent_id,
        'title': 'Original Title'
    })
    assert conv_response.status_code == 201
    conv_data = json.loads(conv_response.data)
    conversation_id = conv_data['id']

    # Update conversation title
    update_response = e2e_client.put(f'/api/conversations/{conversation_id}', json={
        'title': 'Updated Title'
    })
    assert update_response.status_code == 200
    update_data = json.loads(update_response.data)
    assert update_data['title'] == 'Updated Title'

    # Archive conversation
    archive_response = e2e_client.put(f'/api/conversations/{conversation_id}', json={
        'archived': True
    })
    assert archive_response.status_code == 200
    archive_data = json.loads(archive_response.data)
    assert archive_data['archived'] is True

    # Verify archived conversation in user's archived list
    archived_response = e2e_client.get(f'/api/users/{user_id}/conversations?archived=true')
    assert archived_response.status_code == 200
    archived_data = json.loads(archived_response.data)
    assert any(conv['id'] == conversation_id for conv in archived_data)
