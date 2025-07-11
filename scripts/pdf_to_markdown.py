#!/usr/bin/env python3
"""
PDF to Markdown Converter using Docling

This script converts PDF files to markdown format using the docling library.
It supports both single file conversion and batch processing of multiple PDFs.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List
from docling.document_converter import DocumentConverter


class PDFToMarkdownConverter:
    """A class to handle PDF to Markdown conversion using docling."""
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the converter with optional configuration.
        
        Args:
            config: Optional configuration dictionary for DocumentConverter
        """
        self.config = config or {}
        self._converter = DocumentConverter(**self.config)
    
    @property
    def converter(self) -> DocumentConverter:
        """Get the document converter instance."""
        return self._converter
    
    def convert_pdf_to_markdown(self, file_path: str) -> str:
        """
        Convert a PDF file to markdown format.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Markdown content as string
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If conversion fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise ValueError(f"File must be a PDF: {file_path}")
        
        try:
            print(f"Converting {file_path} to markdown...")
            result = self.converter.convert(file_path)
            markdown_content = result.document.export_to_markdown()
            print(f"✓ Successfully converted {file_path}")
            return markdown_content
        except Exception as e:
            print(f"✗ Error converting {file_path}: {str(e)}")
            raise
    
    def convert_and_save(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert PDF to markdown and save to file.
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Optional output path for markdown file
            
        Returns:
            Path to the saved markdown file
        """
        markdown_content = self.convert_pdf_to_markdown(pdf_path)
        
        if output_path is None:
            # Generate output path based on input PDF name
            pdf_file = Path(pdf_path)
            output_path = str(pdf_file.with_suffix('.md'))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✓ Markdown saved to: {output_path}")
        return str(output_path)
    
    def batch_convert(self, pdf_directory: str, output_directory: Optional[str] = None) -> List[str]:
        """
        Convert all PDF files in a directory to markdown.
        
        Args:
            pdf_directory: Directory containing PDF files
            output_directory: Optional output directory for markdown files
            
        Returns:
            List of paths to converted markdown files
        """
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            raise FileNotFoundError(f"Directory not found: {pdf_directory}")
        
        if output_directory:
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = pdf_dir
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in {pdf_directory}")
            return []
        
        converted_files = []
        print(f"Found {len(pdf_files)} PDF files to convert...")
        
        for pdf_file in pdf_files:
            try:
                output_path = output_dir / f"{pdf_file.stem}.md"
                self.convert_and_save(str(pdf_file), str(output_path))
                converted_files.append(str(output_path))
            except Exception as e:
                print(f"✗ Failed to convert {pdf_file}: {str(e)}")
                continue
        
        print(f"✓ Successfully converted {len(converted_files)} out of {len(pdf_files)} files")
        return converted_files


def main():
    """Main function to handle command line arguments and execute conversion."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown using docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single PDF file
  python pdf_to_markdown.py document.pdf
  
  # Convert PDF with custom output path
  python pdf_to_markdown.py document.pdf -o output.md
  
  # Batch convert all PDFs in a directory
  python pdf_to_markdown.py -d /path/to/pdfs
  
  # Batch convert with custom output directory
  python pdf_to_markdown.py -d /path/to/pdfs -o /path/to/output
        """
    )
    
    # Input options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('pdf_file', nargs='?', help='Path to PDF file to convert')
    group.add_argument('-d', '--directory', help='Directory containing PDF files for batch conversion')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output path for markdown file(s)')
    parser.add_argument('--config', help='Path to JSON config file for DocumentConverter')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        import json
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            print(f"Loaded config from {args.config}")
        except Exception as e:
            print(f"Warning: Could not load config file {args.config}: {e}")
    
    try:
        converter = PDFToMarkdownConverter(config)
        
        if args.pdf_file:
            # Single file conversion
            converter.convert_and_save(args.pdf_file, args.output)
        elif args.directory:
            # Batch conversion
            converter.batch_convert(args.directory, args.output)
            
    except KeyboardInterrupt:
        print("\n✗ Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()