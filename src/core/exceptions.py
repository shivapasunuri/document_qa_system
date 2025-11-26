class DocumentQAException(Exception):
    """Base exception for Document Q&A system"""
    pass

class DocumentLoadError(DocumentQAException):
    """Raised when document loading fails"""
    pass

class VectorStoreError(DocumentQAException):
    """Raised when vector store operations fail"""
    pass