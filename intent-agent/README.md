# Intent Agent

Classifies payment disputes into predefined intent categories using GPT-4o-mini.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=sk-proj-your-key-here
```

## Run Locally

### Test the classifier directly:
```bash
python intent_classifier.py
```

### Run the API server:
```bash
python main.py
```

Server will start on http://localhost:8080

## API Endpoints

### POST /classify
Classify a dispute case

**Request:**
```json
{
  "case_id": "CASE-00001",
  "description": "My card was stolen and I see unauthorized charges"
}
```

**Response:**
```json
{
  "case_id": "CASE-00001",
  "intent_code": "INT-11",
  "intent_name": "Lost/Stolen Card",
  "confidence": 0.95,
  "reasoning": "..."
}
```

### GET /health
Health check endpoint

## Intent Categories

- INT-01: Fraudulent Transaction
- INT-02: Item Not Received
- INT-03: Item Not As Described
- INT-04: Canceled Recurring Transaction
- INT-05: Duplicate Processing
- INT-06: Incorrect Transaction Amount
- INT-07: Credit Not Processed
- INT-11: Lost/Stolen Card
- INT-18: Other/Unclassified