from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.core.settings import settings
from app.services.indexing import get_vectorstore


def get_qa_chain(model_name: str):
    retriever = get_vectorstore().as_retriever()

    # Create a prompt template
    template = """Answer the following question based on the provided context:

    - If you need to include mathematical formulas, use `$...$` for inline math and `$$...$$` for block math (not parentheses or brackets).
    - Do not use \\( ... \\) or \\[ ... \\] for math.

    Context: {context}

    Question: {input}

    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    # Detect if model is from LM Studio (adjust logic as needed)
    # Currently, all non-OpenAI models (not prefixed with "gpt-") are from LM Studio
    # TODO: improve this logic
    is_lm_studio = not model_name.startswith("gpt-")

    if is_lm_studio:
        llm = ChatOpenAI(
            model=model_name,
            base_url=f"http://localhost:{settings.lm_studio_port}/v1",
            api_key=SecretStr("lmstudio-placeholder"),  # LM Studio doesn't check the key
        )
    else:
        llm = ChatOpenAI(
            model=model_name,
            api_key=SecretStr(settings.openai_api_key),
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
