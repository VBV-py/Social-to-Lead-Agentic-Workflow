# Inflx: Social-to-Lead Agentic Workflow for AutoStream

This repository contains the solution for building an AI-powered conversational agent for "AutoStream", a fictional SaaS company for automated video editing tools. It handles routing user intents, performing RAG over local pricing plans/policies, and utilizing memory for persistent state to qualify high-intent leads and extract their metadata precisely via mock API tools.

## Requirements and Installation

1. **Clone the repository.**
2. **Create a Virtual Environment (Optional but recommended):**
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
4. **Environment Variables:**
   Make and update the `.env` file with your `GEMINI_API_KEY`. (We use Google's Gemini 1.5 Flash natively for quick reasoning).
   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Agent Locally

Run the CLI chat application:
```bash
python main.py
```

Run in browser:
```bash
streamlit run app.py
```

Try testing the workflow sequentially:
1. *Greeting Flow:* "Hi there!"
2. *RAG Flow:* "Tell me about your pricing plans" or "Do you offer refunds?"
3. *Lead Flow:* "I want the Pro plan for my YouTube channel." -> The agent will prompt for your name and email. Provide them over multiple turns, and observe the `mock_lead_capture` triggering!

---

## Architecture Explanation

This agent is built utilizing **LangGraph** due to its superior capabilities in orchestrating complex, multi-actor state machines compared to standard LangChain Chains or AutoGen. I chose LangGraph because building deterministic, graph-based routing ensures that identifying intents vs executing RAG are explicitly separated, reducing hallucinations. 

State management is handled via a `TypedDict` (`AgentState`). As conversational turns progress, each node reads and mutates this state (e.g., storing missing user parameters like name or email). More importantly, the system persists memory across 5-6 conversation turns by tying the LangGraph execution block to a `MemorySaver()` Checkpointer. By injecting a unique `thread_id` on the client invocation `config`, LangGraph seamlessly retains prior conversation history in its directed cyclic run, meaning the agent innately remembers context from past edges in an interaction session.

## WhatsApp Deployment Question


Integrating this LangGraph Agent with WhatsApp requires exposing the agent locally via a web server like **FastAPI** or **Flask**.

1. **Webhook Endpoint**: We create a POST endpoint (e.g., `/webhook`) and configure it via the Meta Developers Portal to receive incoming messages from the WhatsApp Cloud API.
2. **State & Identity**: When a message comes in, the webhook extracts the sender’s phone number. We use this phone number directly as the `thread_id` in LangGraph's checkpointer configuration to persist their memory across multiple distinct messages natively.
3. **Agent Invocation**: The text message is passed to `app.invoke({"messages": [HumanMessage(content=text)]}, config={"configurable": {"thread_id": phone_number}})`.
4. **Sending Responses**: Once the AI agent replies, its output state is parsed and a POST request is sent back to the WhatsApp API (`https://graph.facebook.com/vX.0/{PHONE_NUM_ID}/messages`) forwarding the response directly into the WhatsApp chat.
