import numpy as np
from app.utils import Embeddeding
from rank_bm25 import BM25Okapi
from app.data import DEVICE_DOCUMENTS
from typing import List, Tuple


def sparse_search (query:str, BM25_indexes:BM25Okapi) -> np.ndarray:
    bm25_scores = BM25_indexes.get_scores(query.lower().split())
    return np.argsort(-bm25_scores)

def dense_search (query:str, embed_docs: np.ndarray) -> np.ndarray:
    embedded_query = Embeddeding([query]).embedded[0]
    dense_scores = embed_docs@embedded_query
    return np.argsort(-dense_scores)

def hybrid_search(query:str, BM25_index: BM25Okapi, embed_docs: np.ndarray, Top_k: int=3)->List[Tuple[str,float]]:
    sparse_rank = sparse_search(query,BM25_index)
    dense_rank = dense_search(query, embed_docs)
    
    sparse_dense_fusion = {}
    k = 60
    
    for rank, sparse_index in enumerate (sparse_rank):
        sparse_dense_fusion[sparse_index] = 1 / (k + rank + 1)
        
    for rank, dense_index in enumerate (dense_rank):
        sparse_dense_fusion[dense_index] = sparse_dense_fusion[dense_index] + (1 / (k + rank + 1))
    
    descending_fusion = sorted(sparse_dense_fusion.items(),key=lambda item: item[1],reverse=True)[:Top_k]

    return [(DEVICE_DOCUMENTS[doc_index], score) for doc_index, score in descending_fusion]
    

    
    