"""
Pydantic models for candidate resume analysis.

This module defines the data models used for analyzing and ranking job candidates
based on their AI/ML experience and well-known software company background.
"""

from pydantic import BaseModel, Field

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
