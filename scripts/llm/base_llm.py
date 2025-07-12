"""
Base LLM functionality using pydantic_ai.

This module provides the base functionality for LLM implementations using
the pydantic_ai framework with Agent-based architecture.
"""

import asyncio
from functools import wraps
from typing import Any, Optional, Type, TypeVar
from pydantic_ai import Agent

T = TypeVar('T')


def async_retry(max_retries, initial_delay):
    def decorator(async_func):
        @wraps(async_func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return await async_func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries:
                        current_delay = initial_delay * (2 ** attempt)
                        await asyncio.sleep(current_delay)
                    else:
                        raise RuntimeError(f"Failed after {max_retries} retries: {str(e)}") from e
            return None  # In case of no retries, though logically unreachable
        return wrapper
    return decorator

class BaseLLM:
    def __init__(self, model):
        self.model = model
        self.agent = Agent(self.model)
    
    @async_retry(max_retries=3, initial_delay=1.0)
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
    
