from fastapi import FastAPI
from app.utils import Embeddeding, BM25_index
from app.schema import ExtractRequest, ExtractResponse, SearchRequest, SearchResponse, SearchResult
from app.services import hybrid_search, extract_device
from app.data import DEVICE_DOCUMENTS


app = FastAPI()

BM25_indexes = BM25_index(DEVICE_DOCUMENTS).BM25_indexes
embed_docs = Embeddeding(DEVICE_DOCUMENTS).embedded

@app.post("/extract", response_model=ExtractResponse)
async def extract(query: ExtractRequest):
    validatedDevice = await extract_device(query.text)
    return validatedDevice


@app.post("/search", response_model=SearchResponse)
def search(query: SearchRequest, top_k: int = 3):
    Documents_Scores = hybrid_search(query.q, BM25_indexes, embed_docs, top_k)
    return SearchResponse(results=[SearchResult(document=doc, score=score) for doc, score in Documents_Scores])




