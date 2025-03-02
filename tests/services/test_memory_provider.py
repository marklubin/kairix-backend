import pytest
import numpy as np
from unittest.mock import Mock, patch
from app.services.memory_provider import VectorMemoryProvider
from app.models import Memory, db

@pytest.fixture
def embedding_service():
    """Create a mock embedding service."""
    service = Mock()
    service.create_embedding.return_value = np.random.rand(1536).tolist()
    return service

@pytest.fixture
def memory_provider(embedding_service):
    """Create a VectorMemoryProvider instance."""
    return VectorMemoryProvider(embedding_service)

def test_get_relevant_memories(app, memory_provider):
    """Test retrieving relevant memories."""
    with app.app_context():
        # Create test memories
        memories = []
        for i in range(5):
            memory = Memory(
                content=f"Test content {i}",
                embedding=np.random.rand(1536).tolist()
            )
            memories.append(memory)
        db.session.add_all(memories)
        db.session.commit()
        
        # Get relevant memories
        query = "test query"
        results = memory_provider.get_relevant_memories(query, limit=3)
        
        # Verify results
        assert len(results) == 3
        assert all(isinstance(m, Memory) for m in results)
        memory_provider.embedding_service.create_embedding.assert_called_once_with(query)

def test_get_relevant_memories_empty(app, memory_provider):
    """Test retrieving memories when none exist."""
    with app.app_context():
        results = memory_provider.get_relevant_memories("test query")
        assert len(results) == 0

def test_get_relevant_memories_limit(app, memory_provider):
    """Test the limit parameter."""
    with app.app_context():
        # Create test memories
        memories = []
        for i in range(5):
            memory = Memory(
                content=f"Test content {i}",
                embedding=np.random.rand(1536).tolist()
            )
            memories.append(memory)
        db.session.add_all(memories)
        db.session.commit()
        
        # Test different limits
        assert len(memory_provider.get_relevant_memories("query", limit=2)) == 2
        assert len(memory_provider.get_relevant_memories("query", limit=10)) == 5
