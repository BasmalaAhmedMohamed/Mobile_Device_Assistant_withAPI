from sentence_transformers import SentenceTransformer
import numpy as np


class Embeddeding:
    def __init__(self, documents: list[str]):
        self.documents = documents
        self.embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.embedded = self.embedding_model.encode(documents, normalize_embeddings=True).astype(np.float32)
        
    def embedding_query(self, query:str):
        return self.embedding_model.encode([query],normalize_embeddings=True)[0].astype(np.float32)


