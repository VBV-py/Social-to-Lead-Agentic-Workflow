from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.state import AgentState
from rag.retriever import retrieve_knowledge
from agent.tools import mock_lead_capture
import json
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

def determine_intent(state: AgentState):
    """LLM node determines if the user intent is casual_greeting, product_inquiry, or high_intent_lead."""
    if state.get("intent") == "high_intent_lead" and not state.get("lead_captured"):
        return {"intent": "high_intent_lead"}

    messages = state["messages"]
    last_user_msg = [m.content for m in messages if isinstance(m, HumanMessage)][-1]
    
    prompt = f"""Analyze user input and determine their intent. MUST be one of:
1. casual_greeting
2. product_inquiry
3. high_intent_lead

User Input: '{last_user_msg}'

Return ONLY the intent string."""
    
    response = llm.invoke(prompt)
    intent = response.content.strip().split("\n")[0].replace("'", "").replace('"', '').strip()
    
    if "high_intent" in intent or "lead" in intent:
        intent = "high_intent_lead"
    elif "product" in intent or "inquiry" in intent or "pricing" in intent:
        intent = "product_inquiry"
    else:
        intent = "casual_greeting"
        
    return {"intent": intent}

def handle_casual(state: AgentState):
    """Handles basic greeting flows."""
    prompt = "You are a friendly AI Agent for AutoStream, a SaaS for automated video editing. Keep it very short, welcome them, and ask how you can help."
    msgs = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.invoke(msgs)
    return {"messages": [response]}

def handle_product_inquiry(state: AgentState):
    """Injects RAG context for answering AutoStream questions."""
    last_user_msg = [m.content for m in state["messages"] if isinstance(m, HumanMessage)][-1]
    context = retrieve_knowledge(last_user_msg)
    
    prompt = f"""You are a helpful AI Agent for AutoStream. Answer their questions ONLY using the retrieved knowledge base context. Keep it concise naturally.

Knowledge Base:
{context}"""
    msgs = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.invoke(msgs)
    return {"messages": [response]}

def handle_high_intent(state: AgentState):
    """Collects minimum parameters iteratively (Name, Email, Platform) before triggering mock_lead_capture tool."""
    prompt = """You are an AI Agent for AutoStream. The user has high intent to use our product.
Collect their Name, Email, and Creator Platform (YouTube, Instagram, etc.). Review the history. Respectfully ask for missing items.
If we have ALL THREE provided by the user, output EXACTLY this JSON format:
{"ready": true, "name": "<name>", "email": "<email>", "platform": "<platform>"}

Otherwise, simply respond to collect the missing info. DO NOT OUTPUT JSON UNLESS ALL THREE FIELDS ARE DEFINITIVELY KNOWN."""
    
    msgs = [SystemMessage(content=prompt)] + state["messages"]
    response = llm.invoke(msgs)
    
    text = response.content.strip()
    
    if text.startswith("{") and text.endswith("}"):
        try:
            clean_text = text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            if data.get("ready"):
                result = mock_lead_capture(data.get("name", ""), data.get("email", ""), data.get("platform", ""))
                return {
                    "user_name": data.get("name"),
                    "user_email": data.get("email"),
                    "user_platform": data.get("platform"),
                    "lead_captured": True,
                    "messages": [AIMessage(content=result)]
                }
        except Exception:
            pass

    return {"messages": [response]}
