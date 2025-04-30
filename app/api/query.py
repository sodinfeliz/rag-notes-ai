from fastapi import APIRouter

from app.models.query_schema import QueryRequest
from app.services.rag_chain import get_qa_chain

router = APIRouter()


@router.post("/query")
async def query_ragnote(req: QueryRequest):
    qa = get_qa_chain()
    response = qa.invoke({"input": req.query})
    return {
        "answer": response["answer"],
        "source_docs": response.get("context", [])
    }
