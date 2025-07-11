#!/usr/bin/env python3
"""
Hello World example for Gemini LLM using pydantic_ai.

This script demonstrates how to use the GeminiLLM class to generate
responses from Google's Gemini models.
"""

import sys
import os
import asyncio

# Add the scripts directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm.gemini import GeminiLLM

async def hello_world_async():
    """Async hello world example."""
    print("🚀 Hello World - Gemini LLM Example (Async)")
    print("=" * 50)
    
    try:
        # Initialize Gemini LLM with gemini-2.0-flash model
        llm = GeminiLLM("gemini-2.0-flash")
        print(f"✅ Initialized Gemini LLM with model: {llm.model_name}")
        
        # Simple hello world prompt
        prompt = "Say hello and introduce yourself as Gemini AI assistant. Keep it brief and friendly."
        
        print(f"\n📝 Prompt: {prompt}")
        print("\n🤖 Gemini Response:")
        print("-" * 30)
        
        # Generate response
        response = await llm.generate(prompt)
        print(response)
        
        print("\n" + "=" * 50)
        print("✨ Hello World example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(hello_world_async())