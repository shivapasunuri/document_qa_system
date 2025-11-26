from typing import List, Union
from pathlib import Path
import pypdf
import os
from langchain_core.documents import Document
from src.core.exceptions import DocumentLoadError

class DocumentLoader:
    """Professional document loader with error handling"""
    
    @staticmethod
    def load_pdf(file_path: Union[str, Path]) -> List[Document]:
        """Load and extract text from PDF files"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return [Document(
                    page_content=text,
                    metadata={"source": str(file_path), "type": "pdf"}
                )]
        except Exception as e:
            raise DocumentLoadError(f"Error loading PDF {file_path}: {str(e)}")
    
    @staticmethod
    def load_directory(directory_path: str) -> List[Document]:
        """Load all PDF files from a directory"""
        docs = []
        directory = Path(directory_path)
        
        for pdf_file in directory.glob("*.pdf"):
            docs.extend(DocumentLoader.load_pdf(pdf_file))
        
        return docs