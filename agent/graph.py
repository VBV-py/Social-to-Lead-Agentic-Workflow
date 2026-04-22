from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agent.state import AgentState
from agent.nodes import determine_intent, handle_casual, handle_product_inquiry, handle_high_intent

def route_intent(state: AgentState):
    """Routes to the correct executable node based on the state's semantic intent string."""
    if state.get("intent") == "casual_greeting":
        return "casual"
    elif state.get("intent") == "product_inquiry":
        return "product_inquiry"
    elif state.get("intent") == "high_intent_lead":
        return "high_intent"
    return "casual" 

workflow = StateGraph(AgentState)

workflow.add_node("determine_intent", determine_intent)
workflow.add_node("casual", handle_casual)
workflow.add_node("product_inquiry", handle_product_inquiry)
workflow.add_node("high_intent", handle_high_intent)

workflow.set_entry_point("determine_intent")
workflow.add_conditional_edges("determine_intent", route_intent)

workflow.add_edge("casual", END)
workflow.add_edge("product_inquiry", END)
workflow.add_edge("high_intent", END)

# Preserves state over recursive edges bounded to specific session threads
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
