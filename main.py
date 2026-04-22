import uuid
import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

def main():
    if not os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") == "your_gemini_api_key_here":
        print("WARNING: Valid GEMINI_API_KEY not found in .env. API calls will fail.")
        sys.exit(1)

    from agent.graph import app

    print("\n=== AutoStream Conversational Agent ===")
    print("Type 'exit' or 'quit' to stop.\n")
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break
            
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
            
        if not user_input.strip():
            continue
            
        messages = [HumanMessage(content=user_input)]
        
        try:
            state = app.invoke({"messages": messages}, config)
            ai_msg = state["messages"][-1].content
            print(f"Agent: {ai_msg}\n")
            
            if state.get("lead_captured"):
                print(">> [System: Lead capture complete. Starting new context thread.]")
                thread_id = str(uuid.uuid4())
                config = {"configurable": {"thread_id": thread_id}}
                
        except Exception as e:
            print(f"Agent Error: {e}")

if __name__ == "__main__":
    main()
