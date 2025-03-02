from abc import ABC, abstractmethod
from typing import List
from app.models import Memory

class MemoryProvider(ABC):
    """Abstract base class for memory providers."""
    
    @abstractmethod
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[Memory]:
        """
        Retrieve relevant memories for a given query.
        
        Args:
            query: The query text to find relevant memories for
            limit: Maximum number of memories to return
            
        Returns:
            List of Memory objects ordered by relevance
        """
        pass

class NoOpMemoryProvider(MemoryProvider):
    """Memory provider that returns no memories. Used as default."""
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[Memory]:
        """Return empty list of memories."""
        return []

class VectorMemoryProvider(MemoryProvider):
    """Memory provider that uses vector similarity search."""
    
    def __init__(self, embedding_service):
        """
        Initialize the vector memory provider.
        
        Args:
            embedding_service: Service for generating embeddings
        """
        self.embedding_service = embedding_service
        
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[Memory]:
        """
        Retrieve relevant memories using vector similarity search.
        
        Args:
            query: The query text to find relevant memories for
            limit: Maximum number of memories to return
            
        Returns:
            List of Memory objects ordered by relevance
        """
        # Generate embedding for the query
        query_embedding = self.embedding_service.create_embedding(query)
        
        # Find similar memories
        return Memory.find_similar(query_embedding, limit=limit)
