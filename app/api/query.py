from fastapi import APIRouter

from app.models.query_schema import QueryRequest
from app.services.indexing import get_vectorstore
from app.services.rag_chain import get_qa_chain

router = APIRouter()


@router.post("/query")
async def query_ragnote(req: QueryRequest):
    qa = get_qa_chain(req.model_name, req.platform)
    response = qa.invoke({"input": req.query})
    return {
        "answer": response["answer"],
        "source_docs": response.get("context", [])
    }

@router.post("/debug_search")
async def debug_search(req: QueryRequest):
    vectorstore = get_vectorstore()
    if not vectorstore:
        return {"error": "Vectorstore not initialized."}

    docs = vectorstore.similarity_search(req.query, k=5)
    return [
        {
            "source": d.metadata.get("source", "unknown"),
            "page_content": d.page_content
        }
        for d in docs
    ]
