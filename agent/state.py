import operator
from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    intent: str 
    user_name: str
    user_email: str
    user_platform: str
    lead_captured: bool
