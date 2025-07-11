"""
Parser module for RAG evaluation.

This module provides functionality to convert various document formats to markdown.
It includes a registry system for parsers and utilities for batch processing documents.
"""

import os
from typing import List
from tqdm import tqdm

from rag_evaluation.config import InputData
from rag_evaluation.utils import get_logger, uuid_from_string, save_json, load_json, ensure_directory

from .base_parser import BaseMDParser
from .docling_parser import DoclingParser
from .markitdown_parser import MarkItDownParser

logger = get_logger(__name__)

def convert_to_md_files(parser_instance: BaseMDParser, input_documents: InputData, md_list_file: str, md_output_dir: str, flag: bool = True) -> List[str]:
    
    ensure_directory(md_list_file)

    if not flag:
        return load_json(md_list_file)
    
    os.makedirs(md_output_dir, exist_ok=True)
    md_list: List[str] = []
    
    try:
        # Process files
        if input_documents.files:
            logger.info(f"Parsing {len(input_documents.files)} source files...")
            md_list.extend(_process_file_list(
                parser_instance, 
                input_documents.files, 
                md_output_dir
            ))
        
        # Process links
        if input_documents.links:
            logger.info(f"Parsing {len(input_documents.links)} source links...")
            md_list.extend(_process_link_list(
                parser_instance, 
                input_documents.links, 
                md_output_dir
            ))
        
        # Save results
        save_json(md_list, md_list_file)
        
        return md_list
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise IOError(f"Failed to process documents: {str(e)}") from e

def _process_file_list(
    parser: BaseMDParser, 
    files: List[str], 
    output_dir: str
) -> List[str]:

    result = []
    for input_file in tqdm(files, desc="Processing files"):
        output_file = os.path.join(output_dir, f'{uuid_from_string(input_file)}.json')
        output = parser.parse_file(input_file, output_file)
        if output:
            result.append(output)
        else:
            logger.warning(f"Failed to parse file: {input_file}")
    return result


def _process_link_list(
    parser: BaseMDParser, 
    links: List[str], 
    output_dir: str
) -> List[str]:
 
    result = []
    for link in tqdm(links, desc="Processing links"):
        output_file = os.path.join(output_dir, f'{uuid_from_string(link)}.json')
        output = parser.parse_link(link, output_file)
        if output:
            result.append(output)
        else:
            logger.warning(f"Failed to parse link: {link}")
    return result

# Define public API
__all__ = ['BaseMDParser', 'DoclingParser', 'MarkItDownParser', 'convert_to_md_files' ]
