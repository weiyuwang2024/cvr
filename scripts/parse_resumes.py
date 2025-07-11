#!/usr/bin/env python3
"""
Resume Parser Script using Docling Parser

This script uses the DoclingParser to parse PDF resume files and generate
candidate reviews using AI/ML analysis.

Usage:
    python scripts/parse_resumes.py --input path/to/resume.pdf
    python scripts/parse_resumes.py --input path/to/resumes/directory/ --output custom_results/
    python scripts/parse_resumes.py -i resumes/ -o results/ --model gpt-4o
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import List,Any
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.parser.docling_parser import DoclingParser
from scripts.llm.openai import OpenAILLM, AVAILABLE_MODELS as AVAILABLE_OPENAI_MODELS
from scripts.llm.gemini import GeminiLLM, AVAILABLE_MODELS as AVAILABLE_GEMINI_MODELS

# Combined available models from both providers
AVAILABLE_MODELS = AVAILABLE_OPENAI_MODELS + AVAILABLE_GEMINI_MODELS


def find_pdf_files(input_path: str) -> List[str]:
    """Find all PDF files in the given path."""
    path = Path(input_path)
    
    if path.is_file() and path.suffix.lower() == '.pdf':
        return [str(path)]
    elif path.is_dir():
        return [str(f) for f in path.glob('**/*.pdf')]
    else:
        return []


async def parse_resume_file(parser: DoclingParser, pdf_path: str, output_dir: str) -> List[Any]:
    """Parse a single resume PDF file."""
    pdf_name = Path(pdf_path).stem
    output_file = os.path.join(output_dir, f"{pdf_name}.json")
    
    print(f"Processing: {pdf_path}")
    results = await parser.parse_file(pdf_path, output_file)
    return results


def print_resume_reviews(candidates: List[Any]) -> None:
    """Print resume reviews from analysis files."""
    print("\n" + "="*80)
    print("RESUME ANALYSIS RESULTS")
    print("="*80)
    
   
    if not candidates:
        print("No candidate data found.")
        return
    
    # Sort candidates by AI/ML score (descending) then by company experience
    candidates.sort(
        key=lambda x: (x.get('ai_ml_experience_score', 0), x.get('well_known_software_company_experience', 0)),
        reverse=True
    )
    
    print(f"\nTotal Candidates Analyzed: {len(candidates)}")
    print("\nRanked Candidate Reviews:")
    print("-" * 80)

    for i, candidate in enumerate(candidates, 1):
        name = candidate.get('name', 'Unknown')
        ai_score = candidate.get('ai_ml_experience_score', 0)
        company_exp = candidate.get('well_known_software_company_experience', 0)
        reason = candidate.get('reason_for_score', 'No reason provided')
        
        print(f"\n{i}. {name}")
        print(f"   AI/ML Experience Score: {ai_score}/10")
        print(f"   Well-Known Company Experience: {company_exp} years")
        print(f"   Analysis: {reason}")
        
        if i < len(candidates):
            print("-" * 40)
    
    # Print summary
    high_ai_candidates = [c for c in candidates if c.get('ai_ml_experience_score', 0) >= 7]
    company_exp_candidates = [c for c in candidates if c.get('well_known_software_company_experience', 0) > 0]

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Candidates with high AI/ML scores (7+): {len(high_ai_candidates)}")
    print(f"Candidates with well-known company experience: {len(company_exp_candidates)}")


async def main():
    """Main function to orchestrate resume parsing and analysis."""
    parser = argparse.ArgumentParser(
        description="Parse resume PDFs and generate candidate reviews using AI analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse single resume
  python scripts/parse_resumes.py --input resume.pdf
  
  # Parse directory of resumes with custom output
  python scripts/parse_resumes.py --input resumes/ --output custom_results/
  
  # Use specific OpenAI model
  python scripts/parse_resumes.py -i resumes/ -o results/ --model gpt-4o
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to PDF file or directory containing PDF files'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='resume_analysis_results',
        help='Output directory for analysis results (default: resume_analysis_results)'
    )
    
    parser.add_argument(
        '--model', '-m',
        choices=AVAILABLE_MODELS,
        default='gemini-2.5-pro',
        help='Model to use (default: gemini-2.5-pro)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Find PDF files
    pdf_files = find_pdf_files(args.input)
    if not pdf_files:
        print(f"No PDF files found in: {args.input}")
        sys.exit(1)
    
    print(f"Found {len(pdf_files)} PDF file(s) to process")
    if args.verbose:
        print(f"Using model: {args.model}")
        print(f"Output directory: {args.output}")
    
    # Initialize LLM and parser
    if args.model in AVAILABLE_OPENAI_MODELS:
        llm = OpenAILLM(args.model)
    elif args.model in AVAILABLE_GEMINI_MODELS:
        llm = GeminiLLM(args.model)
    else:
        print(f"Model {args.model} is not supported. Available models: {AVAILABLE_MODELS}")
        sys.exit(1)
    docling_parser = DoclingParser(llm)
    
    # Process all PDF files
    candidates = []
    for pdf_path in pdf_files:
        results = await parse_resume_file(docling_parser, pdf_path, args.output)
        candidates.extend(results)
    
    # Print results
    print_resume_reviews(candidates)
    print(f"\nAnalysis files saved in: {args.output}")

if __name__ == "__main__":
    asyncio.run(main())