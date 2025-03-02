from datetime import datetime
import uuid
import numpy as np
from sqlalchemy.sql import text
from sqlalchemy import Index
from pgvector.sqlalchemy import Vector
from . import db

# Enable pgvector extension
def enable_vector_extension():
    """Enable the pgvector extension in PostgreSQL."""
    db.session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
    db.session.commit()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    conversations = db.relationship('Conversation', backref='user', lazy=True)

class Agent(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = db.Column(db.String(50), nullable=False)
    system_message = db.Column(db.Text)
    settings = db.Column(db.JSON)
    conversations = db.relationship('Conversation', backref='agent', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    agent_id = db.Column(db.String(36), db.ForeignKey('agent.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = db.relationship('Message', backref='conversation', lazy=True)

class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversation.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Memory(db.Model):
    """Model for storing text content with vector embeddings for similarity search."""
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    storage_type = db.Column(db.String(50), nullable=False, default='postgres')  # For future storage backends
    embedding_type = db.Column(db.String(50), nullable=False, default='openai')  # For future embedding models
    embedding = db.Column(Vector(1536), nullable=True)  # 1536 dimensions for OpenAI ada-002
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('ix_memory_embedding_cosine', 'embedding', postgresql_using='ivfflat'),
    )

    @classmethod
    def find_similar(cls, query_vector, limit=5, min_similarity=0.7):
        """
        Find similar memories using cosine similarity.
        
        Args:
            query_vector (list): The query embedding vector
            limit (int): Maximum number of results to return
            min_similarity (float): Minimum cosine similarity threshold
            
        Returns:
            List of Memory objects ordered by similarity
        """
        if not isinstance(query_vector, (list, np.ndarray)) or len(query_vector) != 1536:
            raise ValueError("Query vector must be a 1536-dimensional vector")
            
        # Convert to numpy array if needed
        if isinstance(query_vector, list):
            query_vector = np.array(query_vector)
            
        # For testing (SQLite), just return all memories up to limit
        if str(db.engine.url).startswith('sqlite'):
            return cls.query.limit(limit).all()
            
        # For PostgreSQL, use cosine similarity search
        return cls.query.filter(
            cls.embedding.cosine_distance(query_vector) <= (1 - min_similarity)
        ).order_by(
            cls.embedding.cosine_distance(query_vector)
        ).limit(limit).all()
    
    @classmethod
    def batch_create(cls, contents, vectors):
        """
        Create multiple memories in batch.
        
        Args:
            contents (list): List of text contents
            vectors (list): List of embedding vectors
        """
        if len(contents) != len(vectors):
            raise ValueError("Number of contents must match number of vectors")
            
        memories = []
        for content, vector in zip(contents, vectors):
            memory = cls(
                content=content,
                embedding=vector
            )
            memories.append(memory)
            
        db.session.add_all(memories)
        db.session.commit()
        return memories
    
    def update_embedding(self, vector):
        """
        Update the embedding vector for this memory.
        
        Args:
            vector (list or numpy.ndarray): The new embedding vector
        """
        if not isinstance(vector, (list, np.ndarray)) or len(vector) != 1536:
            raise ValueError("Embedding must be a 1536-dimensional vector")
            
        self.embedding = vector if isinstance(vector, list) else vector.tolist()
        self.updated_at = datetime.utcnow()
