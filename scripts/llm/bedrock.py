"""
AWS Bedrock LLM implementations using pydantic_ai with Bedrock provider.

This module provides specific AWS Bedrock model implementations following
the pattern established in the reference implementation.
"""

import os
import boto3
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

from .base_llm import BaseLLM

# Available AWS Bedrock models
AVAILABLE_MODELS = [
    "us.anthropic.claude-sonnet-4-20250514-v1:0",
	"us.anthropic.claude-3-7-sonnet-20250219-v1:0",
]

class BedrockLLM(BaseLLM):
    def __init__(self, model_name: str, region_name: str | None = None):
        """Initialize AWS Bedrock LLM with model name and optional region."""
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} is not available. Available models are: {AVAILABLE_MODELS}")
        
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        model = BedrockConverseModel(
            model_name=model_name,
            provider=BedrockProvider(bedrock_client=bedrock_client),
        )
        super().__init__(model)