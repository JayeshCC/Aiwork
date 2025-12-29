import json
import math
from typing import List, Dict, Any
import uuid

class Memory:
    """
    Abstract base class for Agent memory.
    """
    def add(self, text: str, metadata: Dict[str, Any] = None):
        raise NotImplementedError

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        raise NotImplementedError

class VectorMemory(Memory):
    """
    A lightweight, local vector memory implementation.
    Uses simple word overlap (Jaccard similarity) for demonstration to avoid heavy dependencies.
    In production, this would use proper embeddings (e.g., OpenVINO quantized models).
    """
    def __init__(self):
        self.store = []

    def _get_embedding(self, text: str):
        # Mock embedding: set of unique words
        return set(text.lower().split())

    def _similarity(self, query_vec, doc_vec):
        # Jaccard Similarity
        intersection = len(query_vec.intersection(doc_vec))
        union = len(query_vec.union(doc_vec))
        return intersection / union if union > 0 else 0.0

    def add(self, text: str, metadata: Dict[str, Any] = None):
        entry = {
            "id": str(uuid.uuid4()),
            "text": text,
            "vector": self._get_embedding(text),
            "metadata": metadata or {}
        }
        self.store.append(entry)

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        query_vec = self._get_embedding(query)
        
        scored_docs = []
        for doc in self.store:
            score = self._similarity(query_vec, doc["vector"])
            scored_docs.append((score, doc))
        
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k
        return [doc for score, doc in scored_docs[:k] if score > 0]
