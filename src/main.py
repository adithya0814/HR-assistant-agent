import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.config import BACKEND_MODEL_NAME, SYSTEM_CONTEXT

def main():
    # ========== STREAMLIT PAGE CONFIG ==========
    st.set_page_config(page_title="HR Assistant", page_icon="💼")
    st.title("💼 HR Assistant - Sample IT Solutions")
    st.caption("Ask me about leaves, policies, and benefits.")

    # ========== SIDEBAR (CLEANED UP) ==========
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
        st.markdown("### Employee Helpdesk")
        st.markdown("This assistant is connected to the official **HR Policy Document (2025)**.")
        
        st.divider()
        
        # Only "Clear History" remains visible to the user
        if st.button("Start New Conversation"):
            st.session_state.langchain_messages = []
            st.rerun()

    # ========== LANGCHAIN LOGIC ==========

    # 1. Retrieve API Key from Secrets or Environment Variables
    API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

    # 2. Check if Key Exists
    if not API_KEY:
        st.error("⚠️ Server Error: API Key not found. Please contact the administrator to configure 'GEMINI_API_KEY' in secrets.")
        st.stop()

    # 3. Setup Memory
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    if len(msgs.messages) == 0:
        msgs.add_ai_message("Hello! I am Sam. How can I assist you with HR policies today?")

    # 4. Define Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_CONTEXT),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    # 5. Initialize Chain
    try:
        llm = ChatGoogleGenerativeAI(
            model=BACKEND_MODEL_NAME,
            google_api_key=API_KEY,
            temperature=0.3,
            convert_system_message_to_human=True
        )
        
        chain = prompt | llm
        
        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: msgs,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    except Exception as e:
        st.error(f"Internal configuration error: {e}")
        st.stop()

    # 6. Render Chat UI
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    # 7. Handle Input
    if user_input := st.chat_input("Type your question here..."):
        st.chat_message("human").write(user_input)

        with st.chat_message("ai"):
            with st.spinner("Thinking..."):
                try:
                    config = {"configurable": {"session_id": "any"}}
                    response = chain_with_history.invoke({"input": user_input}, config)
                    st.write(response.content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
