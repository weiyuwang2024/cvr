"""
OpenAI LLM implementations using pydantic_ai with Azure OpenAI.

This module provides specific OpenAI model implementations following
the pattern established in the reference implementation.
"""

import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.azure import AzureProvider

from .base_llm import BaseLLM

# Available Azure OpenAI models
AVAILABLE_MODELS = [
    "gpt-4o-mini", 
    "gpt-4o",
    "gpt-4.1",
    "gpt-4.1-mini",
    "o3-mini"
]

class OpenAILLM(BaseLLM):
    
    def __init__(self, model_name: str):
        """Initialize OpenAI LLM with model name."""
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} is not available. Available models are: {AVAILABLE_MODELS}")
        
        self.model_name = model_name
        self.endpoint = os.getenv('AZURE_LLM_ENDPOINT', '')
        self.api_version = os.getenv('AZURE_LLM_API_VERSION', '')
        self.api_key = os.getenv('AZURE_LLM_API_KEY', '')
        
        # Create provider and model
        self.provider = AzureProvider(
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
            api_key=self.api_key
        )
        self.model = OpenAIModel(model_name, provider=self.provider)
        super().__init__(self.model)

