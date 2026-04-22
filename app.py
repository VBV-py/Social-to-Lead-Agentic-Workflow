import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="AutoStream AI Agent", page_icon="🤖")
st.title("AutoStream AI Agent")
st.markdown("💬 Ask me about AutoStream's SaaS video editing plans, or just say hi!")

if not os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY") == "your_gemini_api_key_here":
    st.error("Please add a valid GEMINI_API_KEY to your `.env` file to start chatting.")
    st.stop()

from agent.graph import app

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

if prompt := st.chat_input("What is your question?"):
    st.chat_message("user").markdown(prompt)
    msg = HumanMessage(content=prompt)
    st.session_state.messages.append(msg)

    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    
    with st.spinner("Agent is typing..."):
        try:
            state = app.invoke({"messages": [msg]}, config)
            ai_content = state["messages"][-1].content
            ai_msg = AIMessage(content=ai_content)
            
            with st.chat_message("assistant"):
                st.markdown(ai_content)
                
            st.session_state.messages.append(ai_msg)
            
            if state.get("lead_captured"):
                st.success("Lead explicitly captured by system! Flushing state memory for next user.")
                st.session_state.thread_id = str(uuid.uuid4())
                
        except Exception as e:
            st.error(f"Agent Error: {e}")
