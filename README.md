# AI Teams Inc

Multi-agent AI collaboration system with FastAPI backend and clean web interface.

## Tech Stack
- **Backend:** Python 3.11, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Anthropic Claude Sonnet 4, OpenAI

## Project Structure
```
ai-teams-inc/
├── ai_team.py          # Core AI team logic
├── api.py              # FastAPI backend
├── static/
│   ├── index.html      # Chat interface
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
├── .env                # API keys (not in git)
└── requirements.txt    # Python dependencies
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with API keys:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

5. Run the server:
```bash
python api.py
```

6. Open browser: http://localhost:8000

## Features
- Real-time AI chat interface
- Claude Sonnet 4 integration
- Clean, responsive UI
- Health check endpoint

## Development
- Single-file edit discipline
- Git version control
- Backup system ready