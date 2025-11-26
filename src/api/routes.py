from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import tempfile
from src.api.models import QueryRequest, QueryResponse, DocumentUploadResponse
from src.document_processor.loader import DocumentLoader
from src.document_processor.splitter import DocumentSplitter
from src.vector_store.chroma_manager import ChromaDBManager
from src.chains.qa_chain import AdvancedQAChain
from src.core.config import settings
from pathlib import Path
from contextlib import asynccontextmanager
# Global instances
vector_store = ChromaDBManager()
qa_system = AdvancedQAChain()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to run startup and shutdown tasks."""
    # Startup tasks
    print("Starting up Document Q&A System...")
    # Create vector store collection
    vector_store.create_collection("default")

    # Load any existing PDFs automatically
    print("Looking for PDFs in data directory...")
    loaded_count = load_existing_pdfs()
    print(f"Loaded {loaded_count} PDF files into vector database")

    # Setup QA chain
    qa_system.setup_retrieval_chain(vector_store)
    print("Document Q&A System ready!")

    try:
        yield
    finally:
        pass

app = FastAPI(title="Document Q&A System", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def load_existing_pdfs():
    """Automatically load PDFs from data directory on startup"""
    data_dir = Path("data")
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data directory")
        return 0
    
    processed_count = 0
    for pdf_file in pdf_files:
        try:
            print(f"Loading PDF: {pdf_file.name}")
            
            # Process document
            documents = DocumentLoader.load_pdf(pdf_file)
            splitter = DocumentSplitter()
            chunks = splitter.split_documents(documents)
            
            # Generate embeddings and add to vector store
            embeddings = qa_system.embeddings.embed_documents(
                [chunk.page_content for chunk in chunks]
            )
            vector_store.add_documents(chunks, embeddings)
            processed_count += 1
            print(f"✅ Successfully loaded: {pdf_file.name} ({len(chunks)} chunks)")
            
        except Exception as e:
            print(f"❌ Failed to load {pdf_file.name}: {str(e)}")
    
    return processed_count

"""Startup handled by app lifespan handler"""

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the document database"""
    try:
        if request.collection_name != "default":
            vector_store.create_collection(request.collection_name)
            qa_system.setup_retrieval_chain(vector_store)
        
        response = qa_system.query(request.question)
        return QueryResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process documents"""
    try:
        processed_count = 0
        temp_dir = tempfile.mkdtemp()
        
        for file in files:
            if file.filename.endswith('.pdf'):
                # Save uploaded file
                file_path = os.path.join(temp_dir, file.filename)
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                
                # Process document
                documents = DocumentLoader.load_pdf(file_path)
                splitter = DocumentSplitter()
                chunks = splitter.split_documents(documents)
                
                # Generate embeddings and add to vector store
                embeddings = qa_system.embeddings.embed_documents(
                    [chunk.page_content for chunk in chunks]
                )
                vector_store.add_documents(chunks, embeddings)
                processed_count += 1
        
        return DocumentUploadResponse(
            message="Documents processed successfully",
            documents_processed=processed_count,
            collection_name="default"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Document Q&A System"}