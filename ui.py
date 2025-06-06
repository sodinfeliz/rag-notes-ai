from datetime import datetime

import requests
import streamlit as st

from app.core.settings import settings

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page config
st.set_page_config(
    page_title="RagNoteAI Chat",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/sodinfeliz/rag-notes-ai',
        'Report a bug': 'https://github.com/sodinfeliz/rag-notes-ai/issues',
        'About': '''
        # RagNotesAI

        A RAG-based AI assistant for note taking, powered by:
        - FAISS for efficient vector search
        - LangChain for RAG pipeline
        - Streamlit for beautiful UI

        Features:
        - Chat with your Obsidian notes
        - Real-time document indexing
        - Source tracking and citations

        [GitHub Repository](https://github.com/sodinfeliz/rag-notes-ai)

        ---
        '''
    }
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
            res = requests.post(
                f"http://localhost:{settings.backend_port}/query",
                json={
                    "query": query,
                    "model_name": st.session_state.get("selected_model", settings.llm_model_name)
                }
            )
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

# Fetch available models from backend
@st.cache_data(ttl=10)
def get_available_models():
    try:
        res = requests.get(f"http://localhost:{settings.backend_port}/models")
        if res.status_code == 200:
            return res.json().get("models", [])
        else:
            st.warning("Could not fetch models from backend.")
            return []
    except Exception as e:
        st.warning(f"Error fetching models: {e}")
        return []


with st.sidebar:
    st.header("Model Selection")
    available_models = get_available_models()
    if available_models:
        selected_model = st.selectbox(
            "Choose a model",
            available_models,
            index=available_models.index(st.session_state.get("selected_model", available_models[0]))
        )
        st.session_state["selected_model"] = selected_model
    else:
        st.write("No models available.")
