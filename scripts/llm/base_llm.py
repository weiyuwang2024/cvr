"""
Base LLM functionality using pydantic_ai.

This module provides the base functionality for LLM implementations using
the pydantic_ai framework with Agent-based architecture.
"""

import asyncio
from typing import Any, Optional, Type, TypeVar
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai.providers.google_gla import GoogleGLAProvider

T = TypeVar('T')

class BaseLLM:
    """Base class for LLM implementations using pydantic_ai."""
    
    def __init__(self, model, provider=None):
        """Initialize the base LLM with a model and optional provider."""
        if provider:
            self.model = model.__class__(model.model_name, provider=provider)
        else:
            self.model = model
        self.agent = Agent(self.model)
    
    async def generate_async(self, prompt: str, result_type: Type[T] = str, verbose: bool = False) -> Any:
        if verbose:
            nodes = []
            # Begin an AgentRun, which is an async-iterable over the nodes of the agent's graph
            async with self.agent.iter(prompt, result_type=result_type) as agent_run:
                async for node in agent_run:
                    # Each node represents a step in the agent's execution
                    nodes.append(node)
            print('----------')
            for node in nodes:
                print(node)
                print()
            print('----------')
            return nodes[-1].data.data
        else:
            response = await self.agent.run(prompt, result_type=result_type)
            return response.data
    
