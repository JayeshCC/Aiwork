from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for Language Model integrations.
    
    LLMs provide reasoning capabilities to agents.
    Framework supports multiple backends through this interface.
    """
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text response from prompt.
        
        Args:
            prompt: Input text prompt
            **kwargs: Backend-specific parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If generation fails
        """
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate response from chat history.
        
        Args:
            messages: List of {"role": "user/assistant", "content": "..."}
            **kwargs: Backend-specific parameters
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If generation fails
        """
        pass


class MockLLM(BaseLLM):
    """
    Mock LLM for testing and development.
    
    Returns deterministic responses without requiring API keys.
    Useful for:
    - Unit tests
    - Development without LLM access
    - Demonstration/education
    """
    
    def __init__(self, responses: Optional[Dict[str, str]] = None):
        """
        Initialize mock LLM.
        
        Args:
            responses: Optional dict mapping prompt substrings to responses
                      If None, generates generic responses
        """
        self.responses = responses or {}
        self.call_count = 0
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response based on prompt keywords."""
        self.call_count += 1
        
        # Check for custom responses
        for keyword, response in self.responses.items():
            if keyword.lower() in prompt.lower():
                return response
        
        # Generic response
        return f"[Mock LLM Response] Based on the prompt, I suggest: {prompt[:50]}..."
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate mock response from chat messages."""
        last_message = messages[-1]["content"] if messages else ""
        return self.generate(last_message, **kwargs)


class OpenAILLM(BaseLLM):
    """
    OpenAI API integration (optional).
    
    Only used if openai package installed and API key configured.
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """
        Initialize OpenAI LLM.
        
        Args:
            model: OpenAI model name
            api_key: API key (if None, uses OPENAI_API_KEY env var)
        """
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. "
                "Install with: pip install openai"
            )
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate response from chat messages."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
