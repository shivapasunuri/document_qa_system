# For the most compatible version
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from typing import List, Dict, Any
from src.core.config import settings
from src.core.exceptions import VectorStoreError

class AdvancedQAChain:
    """Production-grade Q&A chain with RAG"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.LLM_MODEL,  # Changed from model to model_name
            temperature=0.1,
            max_tokens=1000
        )
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL
        )
        self.vector_store = None
        
    def setup_retrieval_chain(self, vector_store):
        """Setup the complete RAG chain"""
        self.vector_store = vector_store
        
        # Professional prompt template
        prompt_template = """You are an expert document analysis assistant. 
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}

        Answer: """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        self.chain = (
            {"context": self._retrieve_documents, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _retrieve_documents(self, question: str) -> str:
        """Retrieve relevant documents for the question"""
        if not self.vector_store:
            raise VectorStoreError("Vector store not initialized")
        
        results = self.vector_store.similarity_search(question, k=4)
        return "\n\n".join(results['documents'][0]) if results['documents'] else ""
    
    def query(self, question: str) -> Dict[str, Any]:
        """Execute query with comprehensive response"""
        try:
            answer = self.chain.invoke(question)
            return {
                "answer": answer,
                "status": "success",
                "question": question
            }
        except Exception as e:
            return {
                "answer": None,
                "status": "error",
                "error": str(e),
                "question": question
            }