"""Streamlit UI for chatting with the RagNotesAI backend."""

from __future__ import annotations

from datetime import datetime

import requests
import streamlit as st

from app.core.settings import settings

BASE_URL = f"http://localhost:{settings.backend_port}"


def init_session() -> None:
    """Initialize default values in the Streamlit session state."""

    if "messages" not in st.session_state:
        st.session_state.messages = []


def configure_page() -> None:
    """Set Streamlit page configuration."""

    st.set_page_config(
        page_title="RagNoteAI Chat",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get Help": "https://github.com/sodinfeliz/rag-notes-ai",
            "Report a bug": "https://github.com/sodinfeliz/rag-notes-ai/issues",
            "About": """
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
            """,
        },
    )


def display_messages() -> None:
    """Render all chat messages stored in the session."""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("sources"):
                st.markdown(message["sources"])


def format_sources(source_docs: list[dict]) -> str:
    """Return markdown for the source documents."""

    sources_html = ""
    source_paths = set()
    for doc in source_docs:
        metadata = doc.get("metadata", {})
        source_path = metadata.get("source")
        if source_path and source_path not in source_paths:
            source_paths.add(source_path)
            sources_html += f"* 📎 `{source_path}`\n"
    return sources_html


def fetch_response(query: str) -> tuple[str, list[dict]]:
    """Query the backend and return the answer and source documents."""

    payload = {
        "query": query,
        "model_name": st.session_state.get("selected_model", settings.llm_model_name),
        "platform": st.session_state.get("selected_platform", "default"),
    }
    try:
        res = requests.post(f"{BASE_URL}/query", json=payload)
        res.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network errors
        st.error(f"⚠️ Request failed: {exc}")
        return "", []

    data = res.json()
    return data.get("answer", ""), data.get("source_docs", [])


def handle_query(query: str) -> None:
    """Send the query to the backend and display the response."""

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
    )
    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Thinking..."):
        answer, source_docs = fetch_response(query)

    sources_html = format_sources(source_docs)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources_html,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
    )
    with st.chat_message("assistant"):
        st.write(answer)
        if sources_html:
            st.markdown("**Sources:**")
            st.markdown(sources_html)


@st.cache_data(ttl=10)
def get_available_models() -> tuple[list[str], list[str], str | None]:
    """Return the list of models, their platforms and any error message."""

    try:
        res = requests.get(f"{BASE_URL}/models")
        res.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network errors
        st.warning(f"Error fetching models: {exc}")
        return [], [], None

    data = res.json()
    models = data.get("models", [])
    platforms = data.get("platforms", ["unknown"] * len(models))
    errors = data.get("errors")
    return models, platforms, errors


def sidebar_model_selection() -> None:
    """Render the model selection sidebar."""

    st.header("Model Selection")
    available_models, platforms, model_errors = get_available_models()
    if model_errors:
        st.warning(f"Model fetch errors: {model_errors}")

    if available_models:
        model_options = [f"{m} ({p})" for m, p in zip(available_models, platforms, strict=False)]

        selected_model_name = st.session_state.get("selected_model", available_models[0])
        try:
            selected_index = available_models.index(selected_model_name)
        except ValueError:
            selected_index = 0

        selected_option = st.selectbox(
            "Choose a model",
            model_options,
            index=selected_index,
        )

        selected_model = available_models[model_options.index(selected_option)]
        selected_platform = platforms[model_options.index(selected_option)]
        st.session_state["selected_model"] = selected_model
        st.session_state["selected_platform"] = selected_platform
    else:
        st.write("No models available.")


def main() -> None:
    """Main entry point for the Streamlit application."""

    init_session()
    configure_page()

    st.title("🧠 RagNotesAI")
    st.caption("Talk to your Obsidian notes (powered by FAISS + LangChain)")
    display_messages()

    query = st.chat_input("Ask me anything about your notes...")
    if query:
        handle_query(query)

    with st.sidebar:
        sidebar_model_selection()


if __name__ == "__main__":
    main()

