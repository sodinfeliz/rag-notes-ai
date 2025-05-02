import requests
import streamlit as st

st.set_page_config(page_title="RagNoteAI Chat", page_icon="🧠")

st.title("🧠 RagNoteAI")
st.caption("Talk to your Obsidian notes (powered by your FastAPI + FAISS RAG system)")

query = st.text_input("Ask me anything about your notes:", placeholder="e.g. What is LoRA?")

if st.button("Ask") and query.strip():
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://localhost:8000/query", json={"query": query})
            if res.status_code == 200:
                answer = res.json()["answer"]
                st.success("💡 Answer:")
                st.write(answer)
            else:
                st.error(f"❌ Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
