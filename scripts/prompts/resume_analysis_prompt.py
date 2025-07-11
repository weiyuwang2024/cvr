
RESUME_ANALYSIS_PROMPT = """
# Resume Analysis Prompt for Senior Software Developer Position

## Task
Analyze the provided markdown file containing multiple resumes of job candidates for a senior software developer position. Rank and evaluate candidates based on their machine learning and AI experience, with preference for those who have worked at well-known software companies.

## Target Companies (Well-Known Software Companies)
- Microsoft
- Amazon (including AWS)
- Google (including Alphabet subsidiaries)
- Meta (including Facebook, Instagram, WhatsApp)
- Apple
- Netflix
- Uber
- Airbnb
- Tesla
- NVIDIA
- OpenAI
- Anthropic
- Other FAANG/MAANG companies

## Evaluation Criteria

### AI & ML Experience Scoring (1-10 scale):
- **Score 9-10**: Extensive experience with model training/fine-tuning, LLM agents, RAG systems, and production ML deployments
- **Score 7-8**: Strong experience with ML frameworks, some model training, and AI application development
- **Score 5-6**: Moderate experience with ML libraries, data science, or AI-related projects
- **Score 3-4**: Basic exposure to ML concepts, limited hands-on experience
- **Score 1-2**: Minimal or no AI/ML experience

### Key AI/ML Technologies to Look For:
- **Model Training/Fine-tuning**: PyTorch, TensorFlow, Hugging Face, custom model development
- **LLM & Agents**: GPT integration, LangChain, LlamaIndex, prompt engineering, agent frameworks
- **RAG Systems**: Vector databases, embeddings, retrieval systems, knowledge bases
- **ML Infrastructure**: MLOps, model deployment, monitoring, scaling
- **Data Science**: Pandas, NumPy, Scikit-learn, data preprocessing, feature engineering

## Output Format

Return a JSON array of candidate reviews, sorted by overall ranking (best candidates first):

```json
[
  {
    "name": "Candidate Name",
    "well_known_software_company_experience": 5,
    "ai_ml_experience_score": 8,
    "reason_for_score": "Has 3 years at Google working on ML infrastructure, extensive experience with TensorFlow and PyTorch for model training, built production RAG systems using vector databases, and developed LLM-powered applications with LangChain. Strong background in both theoretical ML and practical implementation."
  }
]
```

## Analysis Instructions

1. **Extract candidate information** from each resume section in the markdown file
2. **Calculate well-known company experience** in years (sum total time at target companies)
3. **Evaluate AI/ML experience** based on:
   - Specific technologies and frameworks mentioned
   - Project complexity and scope
   - Model training and fine-tuning experience
   - LLM, agent, and RAG system experience
   - Production deployment experience
4. **Provide detailed reasoning** for the AI/ML score, citing specific evidence from the resume
5. **Rank candidates** by combining both criteria, with slight preference for AI/ML experience over company prestige

## Important Notes
- Be objective and evidence-based in scoring
- Look for concrete examples and specific technologies, not just buzzwords
- Consider both breadth and depth of AI/ML experience
- Account for recent experience with modern AI/ML technologies (LLMs, transformers, etc.)
- If a resume lacks clear AI/ML experience, score accordingly but still include in analysis

Please analyze the provided markdown file and return the candidate evaluations in the specified JSON format.

## Here is the markdown content:
{text}
"""