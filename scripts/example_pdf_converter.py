#!/usr/bin/env python3
"""
Example usage of the PDF to Markdown converter.

This script demonstrates different ways to use the PDFToMarkdownConverter class.
"""

from pdf_to_markdown import PDFToMarkdownConverter
import os


def example_single_conversion():
    """Example of converting a single PDF file."""
    print("=== Single PDF Conversion Example ===")
    
    # Initialize converter
    converter = PDFToMarkdownConverter()
    
    # Example PDF file path (replace with your actual PDF file)
    pdf_file = "cv/Resume_export_example.pdf"
    
    if os.path.exists(pdf_file):
        try:
            # Convert PDF to markdown and save
            output_file = converter.convert_and_save(pdf_file)
            print(f"Conversion completed! Output saved to: {output_file}")
            
            # You can also get the markdown content directly
            markdown_content = converter.convert_pdf_to_markdown(pdf_file)
            print(f"Markdown content preview (first 200 chars):")
            print(markdown_content[:200] + "..." if len(markdown_content) > 200 else markdown_content)
            
        except Exception as e:
            print(f"Error during conversion: {e}")
    else:
        print(f"PDF file '{pdf_file}' not found. Please provide a valid PDF file path.")


def example_batch_conversion():
    """Example of batch converting multiple PDF files."""
    print("\n=== Batch PDF Conversion Example ===")
    
    # Initialize converter
    converter = PDFToMarkdownConverter()
    
    # Example directory containing PDF files
    pdf_directory = "pdf_files"
    output_directory = "markdown_output"
    
    if os.path.exists(pdf_directory):
        try:
            # Convert all PDFs in the directory
            converted_files = converter.batch_convert(pdf_directory, output_directory)
            print(f"Batch conversion completed! Converted {len(converted_files)} files.")
            for file in converted_files:
                print(f"  - {file}")
        except Exception as e:
            print(f"Error during batch conversion: {e}")
    else:
        print(f"Directory '{pdf_directory}' not found.")


def example_with_custom_config():
    """Example of using the converter with custom configuration."""
    print("\n=== Custom Configuration Example ===")
    
    # Custom configuration for DocumentConverter
    custom_config = {
        # Add any specific docling configuration options here
        # For example, you might configure OCR settings, output format options, etc.
    }
    
    # Initialize converter with custom config
    converter = PDFToMarkdownConverter(config=custom_config)
    
    pdf_file = "example.pdf"
    if os.path.exists(pdf_file):
        try:
            markdown_content = converter.convert_pdf_to_markdown(pdf_file)
            print("Conversion with custom config completed!")
            print(f"Content length: {len(markdown_content)} characters")
        except Exception as e:
            print(f"Error during conversion with custom config: {e}")
    else:
        print(f"PDF file '{pdf_file}' not found.")


def main():
    """Run all examples."""
    print("PDF to Markdown Converter Examples")
    print("=" * 40)
    
    # Run examples
    example_single_conversion()
    example_batch_conversion()
    example_with_custom_config()
    
    print("\n" + "=" * 40)
    print("Examples completed!")
    print("\nTo use the converter from command line:")
    print("python pdf_to_markdown.py your_file.pdf")
    print("python pdf_to_markdown.py -d /path/to/pdf/directory")


if __name__ == "__main__":
    main()