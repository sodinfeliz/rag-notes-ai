from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import OPENAI_MODEL_NAME
from app.services.indexing import get_vectorstore


def get_qa_chain():
    retriever = get_vectorstore().as_retriever()

    # Create a prompt template
    template = """Answer the following question based on the provided context:

    - If you need to include mathematical formulas, use `$...$` for inline math and `$$...$$` for block math (not parentheses or brackets).
    - Do not use \\( ... \\) or \\[ ... \\] for math.

    Context: {context}

    Question: {input}

    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(
        model=OPENAI_MODEL_NAME,
        # api_key="..."
    )

    # Create the document chain
    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )

    # Create the retrieval chain
    qa = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain
    )

    return qa
