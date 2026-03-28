# Email OpenEnv

An OpenEnv environment where an AI agent writes professional emails for real-world workplace situations.

## Tasks
- **Easy**: Write a thank-you email to a colleague
- **Medium**: Write an apology email to your manager
- **Hard**: Write a complaint escalation email to a vendor

## API Endpoints
- `POST /reset` — Start a new task
- `POST /step` — Submit an email and get a score
- `GET /state` — Get current environment state

## Scoring
Emails are scored from 0.0 to 1.0 based on greeting, sign-off, length, and required keywords.

## Setup
```bash
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 7860
```

## Environment Variables
- `API_BASE_URL` — LLM API endpoint
- `MODEL_NAME` — Model to use for inference
- `HF_TOKEN` — Hugging Face API key