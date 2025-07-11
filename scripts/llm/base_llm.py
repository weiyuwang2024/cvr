"""
Base LLM functionality using pydantic_ai.

This module provides the base functionality for LLM implementations using
the pydantic_ai framework with Agent-based architecture.
"""

from typing import Any, Optional, Type, TypeVar
from pydantic_ai import Agent

T = TypeVar('T')

class BaseLLM:
    def __init__(self, model):
        self.model = model
        self.agent = Agent(self.model)
    
    async def generate(self, prompt: str, output_type: Type[T] = str, verbose: bool = False) -> Any:
        if verbose:
            nodes = []
            # Begin an AgentRun, which is an async-iterable over the nodes of the agent's graph
            async with self.agent.iter(prompt, output_type=output_type) as agent_run:
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
            response = await self.agent.run(prompt, output_type=output_type)
            return response.data
    
