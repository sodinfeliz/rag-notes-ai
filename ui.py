from datetime import datetime

import requests
import streamlit as st

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page config
st.set_page_config(
    page_title="RagNoteAI Chat",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        width: 200px !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        width: 200px !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 RagNotesAI")
st.caption("Talk to your Obsidian notes (powered by FAISS + LangChain)")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("sources"):
            st.markdown(message["sources"])

# Chat input
query = st.chat_input("Ask me anything about your notes...")

if query:
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(query)

    # Get AI response
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://localhost:8000/query", json={"query": query})
            if res.status_code == 200:
                data = res.json()
                answer = data.get("answer", "")
                source_docs = data.get("source_docs", [])

                # Format sources
                sources_html = ""
                if source_docs:
                    source_paths = set()
                    for doc in source_docs:
                        metadata = doc.get('metadata', {})
                        source_path = metadata.get('source', None)
                        if source_path and source_path not in source_paths:
                            source_paths.add(source_path)
                            sources_html += f"* 📎 `{source_path}`\n"

                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources_html,
                    "timestamp": datetime.now().strftime("%H:%M")
                })

                # Display assistant message
                with st.chat_message("assistant"):
                    st.write(answer)
                    if sources_html:
                        st.markdown("**Sources:**")
                        st.markdown(sources_html)
            else:
                st.error(f"❌ Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")

# Add a clear chat button in the sidebar
with st.sidebar:
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
