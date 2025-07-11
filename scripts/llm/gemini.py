"""
Gemini LLM implementations using pydantic_ai with Google GLA provider.

This module provides specific Gemini model implementations following
the pattern established in the reference implementation.
"""

import os
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from .base_llm import BaseLLM

# Available Gemini models
AVAILABLE_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.5-pro",
]

class GeminiLLM(BaseLLM):
    def __init__(self, model_name: str):
        """Initialize Gemini LLM with model name."""
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} is not available. Available models are: {AVAILABLE_MODELS}")
        
        self.model_name = model_name
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Create provider and model
        provider = GoogleGLAProvider(api_key=self.api_key)
        model = GeminiModel(model_name, provider=provider)
        super().__init__(model)