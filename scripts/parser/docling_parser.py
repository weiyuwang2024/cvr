"""
Docling-based parser implementation for document conversion to markdown.

This module provides a parser implementation that uses the Docling library
to convert various document formats to markdown.
"""

import os
from typing import Optional, Any

from .base_parser import BaseMDParser
from scripts.llm.base_llm import BaseLLM


class DoclingParser(BaseMDParser):

    def __init__(self, llm: BaseLLM, **kwargs: Any) -> None:
        super().__init__(llm)
        self.config = kwargs
        self._converter: Optional[Any] = None
    
    @property
    def converter(self) -> Any:
        if self._converter is None:
            try:
                # Import here to avoid dependency if not using this parser
                from docling.document_converter import DocumentConverter
                self._converter = DocumentConverter(**self.config)
            except ImportError:
                raise ImportError(
                    "Docling package is not installed. "
                    "Install it with 'pip install docling'"
                )
        return self._converter

    def _parse_file(self, file_path: str) -> str:
        # Convert the document
        result = self.converter.convert(file_path)
        return result.document.export_to_markdown()

