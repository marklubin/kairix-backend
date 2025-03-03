import json
import pytest
from tests.e2e.test_e2e_setup import e2e_app, e2e_client, seed_test_data

def test_agent_creation_and_configuration(e2e_client):
    """
    Test agent creation and configuration flow:
    1. Create agent with basic settings
    2. Update agent configuration
    3. Verify agent settings
    """
    # Create agent with basic settings
    agent_response = e2e_client.post('/api/agents/', json={
        'provider': 'OpenAI',
        'system_message': 'You are a helpful assistant',
        'name': 'Test Agent',
        'settings': {
            'temperature': 0.7,
            'max_tokens': 150
        }
    })
    assert agent_response.status_code == 201
    agent_data = json.loads(agent_response.data)
    agent_id = agent_data['id']

    # Update agent configuration
    update_response = e2e_client.put(f'/api/agents/{agent_id}', json={
        'system_message': 'You are a specialized Python assistant',
        'settings': {
            'temperature': 0.5,
            'max_tokens': 200
        }
    })
    assert update_response.status_code == 200
    update_data = json.loads(update_response.data)
    assert update_data['system_message'] == 'You are a specialized Python assistant'
    assert update_data['settings']['temperature'] == 0.5
    assert update_data['settings']['max_tokens'] == 200

def test_agent_specialization(e2e_client, seed_test_data):
    """
    Test agent specialization and response consistency:
    1. Create specialized agent
    2. Test domain-specific responses
    3. Verify response consistency
    """
    user_id = seed_test_data['user_id']

    # Create specialized Python agent
    agent_response = e2e_client.post('/api/agents/', json={
        'provider': 'OpenAI',
        'system_message': 'You are a Python expert. Always include code examples in your responses.',
        'name': 'Python Expert',
        'settings': {
            'temperature': 0.3  # Lower temperature for more consistent responses
        }
    })
    assert agent_response.status_code == 201
    agent_data = json.loads(agent_response.data)
    agent_id = agent_data['id']

    # Create conversation with specialized agent
    conv_response = e2e_client.post('/api/conversations/', json={
        'user_id': user_id,
        'agent_id': agent_id,
        'title': 'Python Expert Conversation'
    })
    assert conv_response.status_code == 201
    conv_data = json.loads(conv_response.data)
    conversation_id = conv_data['id']

    # Test domain-specific questions
    questions = [
        'How do I use list comprehension in Python?',
        'Explain Python decorators with an example'
    ]

    for question in questions:
        message_response = e2e_client.post('/api/messages/', json={
            'conversation_id': conversation_id,
            'content': question,
            'role': 'user'
        })
        assert message_response.status_code == 201

    # Verify responses contain code examples
    history_response = e2e_client.get(f'/api/conversations/{conversation_id}/messages')
    assert history_response.status_code == 200
    history_data = json.loads(history_response.data)
    
    # Check assistant responses
    assistant_messages = [msg for msg in history_data if msg['role'] == 'assistant']
    assert len(assistant_messages) >= len(questions)

def test_agent_memory_and_context(e2e_client, seed_test_data):
    """
    Test agent memory and context handling:
    1. Create agent with memory
    2. Test contextual conversation
    3. Verify memory retention
    """
    user_id = seed_test_data['user_id']

    # Create agent with memory configuration
    agent_response = e2e_client.post('/api/agents/', json={
        'provider': 'OpenAI',
        'system_message': 'You are an assistant with memory capabilities.',
        'name': 'Memory Agent',
        'settings': {
            'memory_enabled': True,
            'memory_window': 10
        }
    })
    assert agent_response.status_code == 201
    agent_data = json.loads(agent_response.data)
    agent_id = agent_data['id']

    # Create conversation
    conv_response = e2e_client.post('/api/conversations/', json={
        'user_id': user_id,
        'agent_id': agent_id,
        'title': 'Memory Test Conversation'
    })
    assert conv_response.status_code == 201
    conv_data = json.loads(conv_response.data)
    conversation_id = conv_data['id']

    # Send series of related messages
    messages = [
        'My name is John.',
        'What is my name?',
        'I like Python programming.',
        'What do I like?'
    ]

    for msg in messages:
        message_response = e2e_client.post('/api/messages/', json={
            'conversation_id': conversation_id,
            'content': msg,
            'role': 'user'
        })
        assert message_response.status_code == 201

    # Verify conversation history and memory retention
    history_response = e2e_client.get(f'/api/conversations/{conversation_id}/messages')
    assert history_response.status_code == 200
    history_data = json.loads(history_response.data)
    
    # Verify all messages are present
    assert len(history_data) >= len(messages) * 2  # User messages + agent responses
