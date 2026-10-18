from rank_bm25 import BM25Okapi
from contextlib import asynccontextmanager



class BM25_index:
    def __init__(self, documents: list[str]):
        self.documents = documents
        self.tokenized_Docs = [doc.lower().split() for doc in documents]
        self.BM25_indexes = BM25Okapi(self.tokenized_Docs)


