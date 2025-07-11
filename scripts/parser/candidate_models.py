"""
Pydantic models for candidate resume analysis.

This module defines the data models used for analyzing and ranking job candidates
based on their AI/ML experience and well-known software company background.
"""

from pydantic import BaseModel, Field
from typing import List


class CandidateReview(BaseModel):
    """
    Model representing a candidate's evaluation for a senior software developer position.
    
    Attributes:
        name: The candidate's full name
        well_known_software_company_experience: Years of experience at well-known software companies
        ai_ml_experience_score: Score from 1-10 rating AI/ML experience and expertise
        reason_for_score: Detailed explanation of why the AI/ML score was assigned
    """
    
    name: str = Field(
        ..., 
        description="The candidate's full name",
        min_length=1
    )
    
    well_known_software_company_experience: int = Field(
        ...,
        description="Total years of experience at well-known software companies (Microsoft, Amazon, Google, Meta, etc.)",
        ge=0
    )
    
    ai_ml_experience_score: int = Field(
        ...,
        description="AI/ML experience score from 1-10, including model training/fine-tuning and LLM Agent/RAG experience",
        ge=1,
        le=10
    )
    
    reason_for_score: str = Field(
        ...,
        description="Detailed explanation of why the AI/ML experience score was assigned, citing specific evidence",
        min_length=10
    )


class CandidateAnalysisResult(BaseModel):
    """
    Model representing the complete analysis result for all candidates.
    
    Attributes:
        candidates: List of candidate reviews, sorted by ranking (best candidates first)
        total_candidates: Total number of candidates analyzed
        analysis_summary: Brief summary of the analysis process
    """
    
    candidates: List[CandidateReview] = Field(
        ...,
        description="List of candidate reviews, sorted by overall ranking"
    )

    def get_top_candidates(self, n: int = 5) -> List[CandidateReview]:
        """
        Get the top N candidates from the analysis.
        
        Args:
            n: Number of top candidates to return (default: 5)
            
        Returns:
            List of top N candidate reviews
        """
        return self.candidates[:n]
    
    def get_candidates_by_ai_score(self, min_score: int = 7) -> List[CandidateReview]:
        """
        Get candidates with AI/ML score above the specified threshold.
        
        Args:
            min_score: Minimum AI/ML score threshold (default: 7)
            
        Returns:
            List of candidates meeting the score criteria
        """
        return [candidate for candidate in self.candidates 
                if candidate.ai_ml_experience_score >= min_score]
    
    def get_candidates_with_company_experience(self, min_years: int = 1) -> List[CandidateReview]:
        """
        Get candidates with well-known company experience above the specified threshold.
        
        Args:
            min_years: Minimum years of well-known company experience (default: 1)
            
        Returns:
            List of candidates meeting the experience criteria
        """
        return [candidate for candidate in self.candidates 
                if candidate.well_known_software_company_experience >= min_years]