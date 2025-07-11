"""
MarkItDown-based parser implementation for document conversion to markdown.

This module provides a parser implementation that uses the Microsoft MarkItDown library
(https://github.com/microsoft/markitdown) to convert various document formats to markdown.
"""

import os
from typing import Optional, Any

from .base_parser import BaseMDParser
from scripts.llm.base_llm import BaseLLM



class MarkItDownParser(BaseMDParser):

    def __init__(self, llm: BaseLLM, **kwargs: Any) -> None:
        super().__init__(llm)
        self.config = kwargs
        self._converter: Optional[Any] = None
    
    @property
    def converter(self) -> Any:
        if self._converter is None:
            try:
                # Import here to avoid dependency if not using this parser
                from markitdown import MarkItDown
                self._converter = MarkItDown(enable_plugins=True)
            except ImportError:
                raise ImportError(
                    "MarkItDown package is not installed. "
                    "Install it with 'pip install markitdown'"
                )
        return self._converter

    def _parse_file(self, file_path: str) -> str:
        
        try:
            # Microsoft MarkItDown uses a unified API for all document types
            # It automatically detects the file type based on extension or content
            result = self.converter.convert(file_path)
            
            # Return the markdown content
            return result.markdown
            
        except Exception as e:
            logger.error(f"Error converting file {file_path}: {str(e)}")
            raise ValueError(f"Failed to convert document: {str(e)}") from e
