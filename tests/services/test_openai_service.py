import pytest
from unittest.mock import Mock, patch
import openai
from app.services.openai_service import OpenAIService
from app.services.memory_provider import MemoryProvider
from app.models import Memory, Agent

@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses."""
    with patch('openai.ChatCompletion.create') as mock_completion, \
         patch('openai.Embedding.create') as mock_embedding:
        # Mock chat completion
        mock_completion.return_value = {
            "choices": [{
                "message": {"role": "assistant", "content": "Test response"}
            }]
        }
        # Mock embedding
        mock_embedding.return_value = {
            "data": [{
                "embedding": [0.1] * 1536
            }]
        }
        yield {
            "completion": mock_completion,
            "embedding": mock_embedding
        }

@pytest.fixture
def mock_memory_provider():
    """Create a mock memory provider."""
    provider = Mock(spec=MemoryProvider)
    provider.get_relevant_memories.return_value = [
        Memory(content="Relevant memory 1"),
        Memory(content="Relevant memory 2")
    ]
    return provider

@pytest.fixture
def mock_agent():
    """Create a mock agent."""
    return Agent(
        id="test-agent",
        provider="openai",
        system_message="You are a test assistant.",
        settings={
            "model": "gpt-4",
            "temperature": 0.5,
            "max_tokens": 500
        }
    )

@pytest.fixture
def openai_service(app):
    """Create an OpenAIService instance."""
    with app.app_context():
        service = OpenAIService()
        service.config.OPENAI_API_KEY = "test-key"
        return service

def test_default_memory_provider(openai_service):
    """Test that service starts with NoOpMemoryProvider."""
    assert openai_service.memory_provider.get_relevant_memories("test") == []

def test_set_memory_provider(openai_service, mock_memory_provider):
    """Test setting a custom memory provider."""
    openai_service.memory_provider = mock_memory_provider
    assert openai_service.memory_provider == mock_memory_provider

def test_set_memory_provider_none(openai_service):
    """Test setting memory provider to None reverts to NoOp."""
    openai_service.memory_provider = None
    assert openai_service.memory_provider.get_relevant_memories("test") == []

def test_create_chat_completion_with_memory(openai_service, mock_openai, mock_memory_provider, mock_agent):
    """Test chat completion with memory context."""
    openai_service.memory_provider = mock_memory_provider
    messages = [{"role": "user", "content": "Hello"}]
    
    response = openai_service.create_chat_completion(messages, mock_agent)
    
    # Verify memory provider was called
    mock_memory_provider.get_relevant_memories.assert_called_once_with("Hello")
    
    # Verify messages structure
    call_args = mock_openai["completion"].call_args[1]
    assert len(call_args["messages"]) == 3  # System + Memory + User
    assert call_args["messages"][0]["content"] == mock_agent.system_message
    assert "Relevant context" in call_args["messages"][1]["content"]
    assert call_args["messages"][2] == messages[0]

def test_create_chat_completion_without_memory(openai_service, mock_openai, mock_memory_provider, mock_agent):
    """Test chat completion with memory disabled."""
    openai_service.memory_provider = mock_memory_provider
    messages = [{"role": "user", "content": "Hello"}]
    
    response = openai_service.create_chat_completion(messages, mock_agent, include_memory=False)
    
    # Verify memory provider was not called
    mock_memory_provider.get_relevant_memories.assert_not_called()
    
    # Verify messages structure
    call_args = mock_openai["completion"].call_args[1]
    assert len(call_args["messages"]) == 2  # System + User
    assert call_args["messages"][0]["content"] == mock_agent.system_message
    assert call_args["messages"][1] == messages[0]

def test_create_chat_completion_with_agent_settings(openai_service, mock_openai, mock_agent):
    """Test chat completion uses agent settings."""
    messages = [{"role": "user", "content": "Hello"}]
    
    response = openai_service.create_chat_completion(messages, mock_agent)
    
    # Verify agent settings were used
    call_args = mock_openai["completion"].call_args[1]
    assert call_args["model"] == mock_agent.settings["model"]
    assert call_args["temperature"] == mock_agent.settings["temperature"]
    assert call_args["max_tokens"] == mock_agent.settings["max_tokens"]

def test_create_chat_completion_override_settings(openai_service, mock_openai, mock_agent):
    """Test that provided settings override agent settings."""
    messages = [{"role": "user", "content": "Hello"}]
    
    response = openai_service.create_chat_completion(
        messages,
        mock_agent,
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=100
    )
    
    # Verify provided settings were used
    call_args = mock_openai["completion"].call_args[1]
    assert call_args["model"] == "gpt-3.5-turbo"
    assert call_args["temperature"] == 0.8
    assert call_args["max_tokens"] == 100

def test_create_chat_completion_with_functions(openai_service, mock_openai, mock_agent):
    """Test chat completion with function definitions."""
    messages = [{"role": "user", "content": "Hello"}]
    functions = [{"name": "test_func", "description": "A test function"}]
    
    response = openai_service.create_chat_completion(
        messages,
        mock_agent,
        functions=functions,
        function_call="auto"
    )
    
    # Verify function calling parameters
    call_args = mock_openai["completion"].call_args[1]
    assert call_args["functions"] == functions
    assert call_args["function_call"] == "auto"

def test_create_embedding(openai_service, mock_openai):
    """Test creating embeddings."""
    embedding = openai_service.create_embedding("Test text")
    
    assert len(embedding) == 1536
    mock_openai["embedding"].assert_called_once_with(
        input="Test text",
        model="text-embedding-ada-002"
    )

def test_create_chat_completion_error(openai_service, mock_agent):
    """Test error handling in chat completion."""
    with patch('openai.ChatCompletion.create', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            openai_service.create_chat_completion(
                [{"role": "user", "content": "Hello"}],
                mock_agent
            )
        assert "OpenAI API error" in str(exc_info.value)

def test_create_embedding_error(openai_service):
    """Test error handling in embedding creation."""
    with patch('openai.Embedding.create', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            openai_service.create_embedding("Test text")
        assert "OpenAI API error" in str(exc_info.value)
