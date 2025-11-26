import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Optional
import uuid
from langchain_core.documents import Document
from src.core.config import settings
from src.core.exceptions import VectorStoreError

class ChromaDBManager:
    """Professional vector store manager with persistence"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = None
    
    def create_collection(self, collection_name: str):
        """Create or get existing collection"""
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise VectorStoreError(f"Error creating collection: {str(e)}")
    
    def add_documents(self, documents: List[Document], embeddings: List[List[float]]):
        """Add documents to vector store with error handling"""
        if not self.collection:
            raise VectorStoreError("Collection not initialized")
        
        try:
            # Convert documents to format for ChromaDB
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas,
                embeddings=embeddings
            )
        except Exception as e:
            raise VectorStoreError(f"Error adding documents: {str(e)}")
    
    def similarity_search(self, query: str, k: int = 4):
        """Perform similarity search with metadata filtering"""
        if not self.collection:
            raise VectorStoreError("Collection not initialized")
        
        return self.collection.query(
            query_texts=[query],
            n_results=k
        )