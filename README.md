# Agentic SOW Generator

A full-stack AI-powered tool to dynamically generate Statements of Work (SOW) using agentic workflows and memory-based retrieval.

## Tech Stack

- **Frontend**: React, Typescript, shadcn-ui  
- **Backend**: Python, Flask  
- **AI Orchestration**: LangGraph  
- **Vector DB**: pgvector (PostgreSQL)  

## System Architecture & Workflow

### Agentic Workflow Overview

This application uses LangGraph to orchestrate multiple specialized AI agents in a workflow pattern:

1. **Multi-Agent Architecture**:
   - **DraftingAgent**: Creates the initial SOW based on user inputs
   - **ComplianceAgent**: Checks if the SOW meets compliance requirements
   - **ValidationAgent**: Validates the SOW structure and data
   - **FormattingAgent**: Converts the validated SOW to a formatted document

2. **Workflow Graph**:
   The agents form a directed graph that processes SOW generation in the following sequence:
   ```
   START → get_relevant_context → drafting_agent → compliance_agent → validation_agent → [conditional routing] → formatting_agent → END
   ```

3. **Vector Database Integration**:
   - Uses pgvector to store embeddings of sample SOW documents
   - Provides relevant context from similar SOWs during drafting
   - Enhances output quality by drawing from existing examples

4. **How It Works in Practice**:
   - User fills out project details in the UI
   - The LangGraph workflow retrieves relevant context from the vector database
   - Agents collaborate to draft, check compliance, validate, and format the SOW
   - If issues arise, the workflow loops back to refine the content
   - The final document is returned as both formatted text and a DOCX file

### Key Features

- **Intelligent Context Retrieval**: Uses vector similarity search to find relevant examples
- **Compliance Checking**: Ensures SOWs meet required standards and regulations
- **Validation & Error Recovery**: Validates content structure with automatic error correction
- **Chat-based Refinement**: Users can refine the generated SOW through conversational interactions
- **Document Export**: Generates professionally formatted DOCX documents

## UI Setup (React)

```bash
cd client
yarn install
yarn run dev
```

Make sure to update the API_BASE_URL in `client\src\features\SOWGenerator\constants.tsx` with the url server is running at.

## Server Setup (Python + Flask + LangGraph)

```bash
cd server
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 1. Setup Environment Variables

Create a `.env` file in the root of `/server` based on `.env-example`:

```bash
cp .env-example .env
```

Update the required keys (e.g., OpenAI API Key, DB connection string).

### 2. Setup PostgreSQL with pgvector

Ensure your PostgreSQL instance has the `pgvector` extension enabled:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Create necessary tables using your preferred method or provided migrations (if any).

### 3. Run vector migrations

```bash
python generate_sample_embeddings.py
```

### 4. Run the Server

```bash
python app.py
```

The Flask server will start and handle LangGraph-based multi-agent interactions and vector DB retrieval.

---

## Core Components

### Server Components

- **Agent Modules** (`/agents`):
  - `drafting_agent.py`: Generates initial SOW content using LLM and vector context
  - `compliance_agent.py`: Checks for required fields and legal/regulatory compliance
  - `validation_agent.py`: Validates SOW structure and data formatting
  - `formatting_agent.py`: Converts validated SOW to formatted documents

- **Graph Orchestration** (`/graph`):
  - `sow_graph.py`: Defines the LangGraph workflow and state management

- **Services** (`/services`):
  - `llm_service.py`: Handles LLM interactions
  - `vector_service.py`: Manages vector database operations

### UI Components

- **SOW Generator** (`/features/SOWGenerator`):
  - Form interface for user input
  - Document preview and chat-based refinement
  - Export functionality for generated documents

## Notes

- Ensure both client and server are running simultaneously.  
- You may need to allow CORS depending on deployment.  
- This project assumes access to OpenAI or Hugging Face for LLM calls.
- The workflow has a built-in retry mechanism (max 10 attempts) for handling errors.