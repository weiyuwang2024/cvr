"""
Base parser module for document conversion to markdown.

This module defines the abstract base class that all document parsers must implement.
"""

from abc import ABC, abstractmethod
import os
from typing import List, Any
import json

from scripts.llm.base_llm import BaseLLM
from scripts.parser.candidate_models import CandidateAnalysisResult
from scripts.prompts import RESUME_ANALYSIS_PROMPT

def ensure_directory(file_path: str) -> str:
    if not file_path:
        raise ValueError("File path cannot be empty")
        
    try:
        directory = os.path.dirname(os.path.abspath(file_path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        return directory
    except Exception as e:
        raise IOError(f"Failed to create directory for {file_path}: {str(e)}") from e

def load_json(file_path: str) -> List[str]:
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
            
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {file_path}")
       
def save_json(data: List[Any], file_path: str) -> None:

    try:
        ensure_directory(file_path)
        
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        raise IOError(f"Failed to save file: {str(e)}") from e

def load_text(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            text = f.read()
            
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise IOError(f"Failed to read text file: {str(e)}") from e
    
def save_text(text: str, file_path: str) -> None:
    try:
        ensure_directory(file_path)
        
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(text)
            
    except Exception as e:
        raise IOError(f"Failed to save text file: {str(e)}") from e

class BaseMDParser(ABC):
    def __init__(self, llm: BaseLLM) -> None:
        self.llm = llm

    @abstractmethod
    def _parse_file(self, file_path: str) -> str:
        pass

    async def parse_file(self, file_path: str, output_file: str) -> List[Any]:
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            if os.path.exists(output_file):
                review_results = load_json(output_file)
                return review_results

            md_file = output_file.replace('.json', '.md')
            
            if os.path.exists(md_file):
                print(f"Markdown file already exists: {md_file}")
                markdown_content = load_text(md_file)
            else:
                # Convert the document
                markdown_content = self._parse_file(file_path)
                save_text(markdown_content, md_file)
            
            prompt = RESUME_ANALYSIS_PROMPT.format(text=markdown_content)
            review_results = await self.llm.generate(prompt, output_type=CandidateAnalysisResult)
            review_results = [r.__dict__ for r in review_results.candidates]
            save_json(review_results, output_file)

            return review_results
            
        except Exception as e:
            return []