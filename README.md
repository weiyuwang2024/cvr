# Resume Parser

A Python script that parses PDF resumes and generates AI-powered candidate analysis with scoring and rankings.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - `GEMINI_API_KEY` - Your Google Gemini API key
   - `AZURE_LLM_ENDPOINT` - Your Azure OpenAI endpoint (optional)
   - `AZURE_LLM_API_KEY` - Your Azure OpenAI API key (optional)

## Usage

### Parse a single resume:
```bash
python scripts/parse_resumes.py --input resume.pdf
```

### Parse multiple resumes from a directory:
```bash
python scripts/parse_resumes.py --input resumes/ --output results/
```

### Use a specific AI model:
```bash
python scripts/parse_resumes.py --input resumes/ --model gpt-4o
```

## Command Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--input` | `-i` | Path to PDF file or directory | Required |
| `--output` | `-o` | Output directory for results | `resume_analysis_results` |
| `--model` | `-m` | AI model to use | `gemini-2.5-pro` |
| `--verbose` | `-v` | Enable detailed output | False |

## Available Models

### Gemini Models
- `gemini-2.0-flash`
- `gemini-2.5-pro`

### OpenAI Models (Azure)
- `gpt-4o-mini`
- `gpt-4o`
- `gpt-4.1`
- `gpt-4.1-mini`
- `o3-mini`

### AWS Bedrock Models
- `us.anthropic.claude-sonnet-4-20250514-v1:0`
- `us.anthropic.claude-3-7-sonnet-20250219-v1:0`

## Output

The script generates:
- Individual JSON analysis files for each resume
- Console output with ranked candidate reviews
- Scoring based on AI/ML experience and company background

### Sample Output:
```
RESUME ANALYSIS RESULTS
================================================================================

Total Candidates Analyzed: 3

Ranked Candidate Reviews:
--------------------------------------------------------------------------------

1. John Smith
   AI/ML Experience Score: 8/10
   Well-Known Company Experience: 3 years
   Analysis: Strong background in machine learning with experience at Google...
```

## Examples

```bash
# Basic usage
python scripts/parse_resumes.py -i candidate_resumes/

# Custom output directory
python scripts/parse_resumes.py -i resumes/ -o analysis_2024/

# Use OpenAI with verbose output
python scripts/parse_resumes.py -i resumes/ -m gpt-4o -v