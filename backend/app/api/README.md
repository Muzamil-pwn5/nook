# FYP Agentic AI Platform

An Agentic AI platform for e-commerce operations.

The system allows AI agents to understand customer requests, use controlled business tools, execute authorized actions, and request human approval for higher-risk actions.

## Current Features

- FastAPI backend
- PostgreSQL database
- Product catalog
- Customer management
- Order creation
- Inventory management
- Agent orchestrator
- Customer Operations Agent
- Conversation state and memory
- Tool registry
- Permission and approval system
- Audit logging
- Browser-accessible API through Swagger
- Automated tests

## Project Structure

fyp-ai-agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── database/
│   │   ├── llm/
│   │   ├── logging/
│   │   ├── permissions/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tools/
│   │   └── main.py
│   │
│   └── tests/
│
├── .gitignore
└── README.md

## Requirements

- Python 3.13+
- PostgreSQL 18+
- Git
- VS Code (recommended)

## Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd fyp-ai-agent

## Create Python Virtual Environment

py -3.13 -m venv .venv

Activate on Windows:

.\.venv\Scripts\Activate.ps1

## Install Dependencies

From the backend directory:

cd backend
python -m pip install -r requirements.txt

## Configure PostgreSQL

Create a PostgreSQL database and application user.

Example:

CREATE USER fyp_app WITH PASSWORD 'YOUR_PASSWORD';
CREATE DATABASE fyp_agent_db OWNER fyp_app;

## Environment Variables

Create:

backend/.env

Add:

DATABASE_URL=postgresql+psycopg://fyp_app:YOUR_PASSWORD@localhost:5432/fyp_agent_db

Do NOT commit .env to GitHub.

## Initialize the Database

From the backend directory:

python -c "from app.database.connection import create_tables; create_tables(); print('Database tables created successfully.')"

## Seed Sample Products

python -m app.database.seed

## Run the Backend

From the backend directory:

python -m uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000

## API Documentation

Open:

http://127.0.0.1:8000/docs

Swagger provides an interactive interface for testing the API.

## Example Agent Workflow

Customer request
↓
Agent decision
↓
Product search
↓
Conversation state
↓
Customer selects product
↓
Customer information
↓
Order request
↓
Permission check
↓
Human approval
↓
Order creation
↓
Inventory update
↓
Audit log

Example customer request:

"I need a laptop under $650"

The agent searches the product catalog.

Then:

"Buy that one"

The agent remembers the selected product and prepares the order.

The order cannot be created until the approval system authorizes the action.

## Run Tests

From the backend directory:

python -m pytest -q

## Security

The following must NOT be committed:

- .env
- Database passwords
- API keys
- .venv
- Local logs containing sensitive information

The .gitignore file is configured to prevent sensitive environment configuration from being uploaded.

## Development Status

This project is under active development.

Current roadmap:

1. Core e-commerce tools
2. Agent orchestration
3. Human approval
4. LLM integration
5. Frontend interface
6. Marketing Agent
7. Evaluation and reliability testing
8. Multi-agent communication

## Architecture Principle

The LLM should not directly access or modify the database.

LLM
↓
Agent
↓
Orchestrator
↓
Permission Layer
↓
Controlled Tool
↓
Database

This provides a controlled boundary between AI reasoning and business operations.

## Team

Final-year project development team.

Repository owner:

Muzamil Abbas