import openai
from typing import List, Dict, Optional, Any
from app.config import get_config
from app.models import Agent
from .memory_provider import MemoryProvider, NoOpMemoryProvider

class OpenAIService:
    """Service for interacting with OpenAI's API."""
    
    def __init__(self, config=None):
        """
        Initialize the OpenAI service.
        
        Args:
            config: Optional configuration object
        """
        self.config = config or get_config()
        openai.api_key = self.config.OPENAI_API_KEY
        self.default_model = self.config.OPENAI_DEFAULT_MODEL
        self.default_temperature = self.config.OPENAI_DEFAULT_TEMPERATURE
        self.default_max_tokens = self.config.OPENAI_DEFAULT_MAX_TOKENS
        self._memory_provider = NoOpMemoryProvider()
        
    @property
    def memory_provider(self) -> MemoryProvider:
        """Get the current memory provider."""
        return self._memory_provider
        
    @memory_provider.setter
    def memory_provider(self, provider: Optional[MemoryProvider]):
        """Set a new memory provider."""
        self._memory_provider = provider if provider is not None else NoOpMemoryProvider()
        
    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        agent: Agent,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[str] = None,
        include_memory: bool = True
    ) -> Dict:
        """
        Create a chat completion using OpenAI's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            agent: Agent instance to use for system message and settings
            model: OpenAI model to use (defaults to config value)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            functions: List of function definitions
            function_call: Control over function calling
            include_memory: Whether to include relevant memories in context
            
        Returns:
            OpenAI API response dictionary
        """
        # Create a new messages list starting with system message
        final_messages = [{
            "role": "system",
            "content": agent.system_message or "You are a helpful assistant."
        }]
        
        # Add memory context if needed
        if include_memory and messages:
            # Get the latest user message
            latest_user_msg = next(
                (msg["content"] for msg in reversed(messages) if msg["role"] == "user"),
                None
            )
            
            if latest_user_msg:
                # Get relevant memories
                memories = self.memory_provider.get_relevant_memories(latest_user_msg)
                
                if memories:
                    # Format memories as context
                    memory_text = "Relevant context:\n" + "\n".join(
                        f"- {memory.content}" for memory in memories
                    )
                    
                    # Add memory context after system message
                    final_messages.append({
                        "role": "system",
                        "content": memory_text
                    })
        
        # Add the user messages
        final_messages.extend(messages)
        
        # Get model settings from agent if not provided
        settings = agent.settings or {}
        if model is None:
            model = settings.get('model', self.default_model)
        if temperature is None:
            temperature = settings.get('temperature', self.default_temperature)
        if max_tokens is None:
            max_tokens = settings.get('max_tokens', self.default_max_tokens)
        
        # Prepare request parameters
        params = {
            "model": model,
            "messages": final_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Add function calling if provided
        if functions:
            params["functions"] = functions
            if function_call:
                params["function_call"] = function_call
                
        try:
            response = openai.ChatCompletion.create(**params)
            return response
            
        except Exception as e:
            # Re-raise with standardized error message
            raise Exception(f"OpenAI API error: {str(e)}")
        
    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding for the given text using OpenAI's API.
        
        Args:
            text: The text to create an embedding for
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response["data"][0]["embedding"]
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
