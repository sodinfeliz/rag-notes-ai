import requests
import streamlit as st

st.set_page_config(page_title="RagNoteAI Chat", page_icon="🧠")

st.title("🧠 RagNoteAI")
st.caption("Talk to your Obsidian notes (powered by FAISS + LangChain)")

# === Update Index Button ===
if st.button("🔄 Update Index"):
    with st.spinner("Updating index..."):
        try:
            res = requests.post("http://localhost:8000/update_index")
            if res.status_code == 200:
                result = res.json()
                st.success(f"✅ Index updated! {len(result['updated_files'])} files changed.")
            else:
                st.error(f"❌ Failed to update: {res.status_code}")
        except Exception as e:
            st.error(f"⚠️ Update failed: {e}")

st.markdown("---")

# === Query Input ===
query = st.text_input("Ask me anything about your notes:", placeholder="e.g. What is LoRA?")

if st.button("Ask") and query.strip():
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://localhost:8000/query", json={"query": query})
            if res.status_code == 200:
                data = res.json()
                answer = data.get("answer", "")
                source_docs = data.get("source_docs", [])

                st.success("💡 Answer:")
                st.write(answer)

                if source_docs:
                    st.markdown("---")
                    st.markdown("📎 **Sources:**")

                    source_paths = set()
                    for doc in source_docs:
                        metadata = doc.get('metadata', {})
                        source_path = metadata.get('source', None)
                        if source_path and source_path not in source_paths:
                            source_paths.add(source_path)
                            st.markdown(f"**{len(source_paths)}.** `{source_path}`")
            else:
                st.error(f"❌ Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
