# Social-to-Lead Agentic Workflow

An AI-powered conversational agent built with **LangGraph** that intelligently routes user interactions and captures high-intent leads for AutoStream, a SaaS platform for automated video editing.

## Overview

This agent demonstrates a multi-turn conversational AI system that:
- **Understands user intent** (casual greeting, product inquiry, high-intent lead)
- **Retrieves contextual knowledge** about products, pricing, and policies
- **Captures lead information** through natural, multi-turn conversations
- **Maintains conversation state** across sessions using LangGraph's memory checkpointer

## Features

- 🤖 **Intent-based Routing**: Automatically categorizes user messages into casual, product inquiry, or high-intent lead flows
- 📚 **RAG Integration**: Retrieves product information from a local knowledge base
- 💬 **Multi-turn Conversations**: Collects user information (name, email, platform) iteratively
- 🧠 **Stateful Memory**: Maintains conversation history per user thread using LangGraph's memory saver
- 🚀 **Dual Interface**: CLI and Streamlit web UI support

## Architecture

The agent is structured around **LangGraph's StateGraph**:

```
determine_intent (entry point)
    ↓
route_intent (conditional)
    ├→ casual_greeting → END
    ├→ product_inquiry → END
    └→ high_intent_lead → END
```

**State Management**: AgentState (TypedDict) tracks:
- `messages`: Conversation history
- `intent`: Current user intent classification
- `user_name`, `user_email`, `user_platform`: Lead information
- `lead_captured`: Boolean flag for lead completion

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VBV-py/Social-to-Lead-Agentic-Workflow.git
   cd Social-to-Lead-Agentic-Workflow
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### CLI Mode
Run the command-line chat interface:
```bash
python main.py
```

### Web UI (Streamlit)
Launch the browser-based interface:
```bash
streamlit run app.py
```

## Testing the Workflows

Try these interactions sequentially to test all agent capabilities:

1. **Greeting Flow:**
   ```
   User: Hi there!
   ```
   Expected: Friendly greeting and offer to help

2. **Product Inquiry Flow:**
   ```
   User: Tell me about your pricing plans
   User: Do you offer refunds?
   ```
   Expected: Agent retrieves and presents pricing/policy information from knowledge base

3. **Lead Capture Flow:**
   ```
   User: I want the Pro plan for my YouTube channel
   Agent: Asks for your name
   User: My name is John Doe
   Agent: Asks for your email
   User: john@example.com
   Agent: Leads captured successfully!
   ```
   Expected: `mock_lead_capture()` is triggered and lead information is logged

## Project Structure

```
.
├── agent/
│   ├── graph.py           # LangGraph workflow definition
│   ├── nodes.py           # Node handlers (intent, casual, inquiry, high-intent)
│   ├── state.py           # AgentState TypedDict definition
│   └── tools.py           # Utility functions (mock_lead_capture)
├── rag/
│   └── retriever.py       # Knowledge base retrieval logic
├── data/
│   └── knowledge_base.json # Product info and policies
├── app.py                 # Streamlit UI
├── main.py                # CLI interface
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## Key Components

### Nodes

- **determine_intent**: Classifies user input using Gemini LLM
- **handle_casual**: Responds to casual greetings
- **handle_product_inquiry**: Retrieves knowledge base and answers product questions
- **handle_high_intent**: Iteratively collects lead information (name, email, platform)

### Knowledge Base

Located in `data/knowledge_base.json`, contains:
- Pricing plans (Basic, Pro)
- Feature lists
- Company policies

### Lead Capture

When all required information is collected, `mock_lead_capture()` is triggered to log the lead.

## Technology Stack

- **LangGraph**: State machine orchestration
- **LangChain**: LLM framework
- **Google Gemini 2.5 Flash**: LLM provider
- **Streamlit**: Web UI framework
- **Python 3.8+**: Runtime

## License

This project is open source and available under the MIT License.

## Author

VBV-py
