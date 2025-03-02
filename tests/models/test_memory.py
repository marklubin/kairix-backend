import pytest
import numpy as np
from app.models import db, Memory

@pytest.fixture
def sample_vector():
    """Create a sample embedding vector."""
    return np.random.rand(1536).tolist()

def test_create_memory(app, sample_vector):
    """Test creating a new memory with embedding."""
    with app.app_context():
        memory = Memory(
            content="Test content",
            embedding=sample_vector
        )
        db.session.add(memory)
        db.session.commit()

        saved = Memory.query.first()
        assert saved.content == "Test content"
        assert saved.storage_type == "postgres"
        assert saved.embedding_type == "openai"
        assert np.allclose(saved.embedding, sample_vector)

def test_find_similar_memories(app, sample_vector):
    """Test finding similar memories using vector similarity."""
    with app.app_context():
        # Create target memory with known vector
        target = Memory(
            content="Target content",
            embedding=sample_vector
        )
        
        # Create memories with random vectors
        other_memories = [
            Memory(
                content=f"Content {i}",
                embedding=np.random.rand(1536).tolist()
            ) for i in range(5)
        ]
        
        db.session.add(target)
        db.session.add_all(other_memories)
        db.session.commit()

        # Search with the same vector - target should be most similar
        results = Memory.find_similar(sample_vector, limit=3)
        assert len(results) > 0
        assert results[0].content == "Target content"

def test_batch_create_memories(app):
    """Test creating multiple memories in batch."""
    with app.app_context():
        contents = ["Content 1", "Content 2"]
        vectors = [np.random.rand(1536).tolist() for _ in range(2)]

        memories = Memory.batch_create(
            contents=contents,
            vectors=vectors
        )

        assert len(memories) == 2
        saved = Memory.query.all()
        assert len(saved) == 2
        assert {m.content for m in saved} == set(contents)

def test_update_embedding(app, sample_vector):
    """Test updating a memory's embedding."""
    with app.app_context():
        memory = Memory(
            content="Test content",
            embedding=sample_vector
        )
        db.session.add(memory)
        db.session.commit()

        new_vector = np.random.rand(1536).tolist()
        memory.update_embedding(new_vector)
        db.session.commit()

        updated = Memory.query.first()
        assert np.allclose(updated.embedding, new_vector)

def test_invalid_vector_dimension(app):
    """Test validation of vector dimensions."""
    with app.app_context():
        with pytest.raises(ValueError):
            memory = Memory(
                content="Test content",
                embedding=[1.0, 2.0]  # Wrong dimension
            )
            memory.update_embedding([1.0, 2.0])  # Should raise ValueError
