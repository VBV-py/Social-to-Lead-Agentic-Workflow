import json

def get_knowledge_base():
    try:
        with open("data/knowledge_base.json", "r") as f:
            return json.load(f)
    except Exception as e:
        return f"Error loading knowledge base: {e}"

def retrieve_knowledge(query: str):
    """Simplified RAG-powered Knowledge Retrieval module fetching directly from local JSON store."""
    kb = get_knowledge_base()
    if isinstance(kb, str):
        return kb
    
    return f"""AutoStream Details:
---
Pricing and Features:
Basic Plan: {kb['pricing_and_features']['basic_plan']}
Pro Plan: {kb['pricing_and_features']['pro_plan']}
---
Company Policies:
{chr(10).join(kb['company_policies'])}"""
