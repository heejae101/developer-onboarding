"""
RAG Modules for Project Rules
"""
import os
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
from src.llm.client import get_llm_client, get_embedding_client

class RuleLoader:
    """Loads and chunks markdown files from rules directory"""
    
    def __init__(self, rules_dir: str = "/Users/chaehuijae/Desktop/가이드/rules"):
        self.rules_dir = Path(rules_dir)
        
    def load_rules(self) -> List[Dict[str, Any]]:
        """Load all markdown files and split into chunks"""
        chunks = []
        
        if not self.rules_dir.exists():
            print(f"Warning: Rules directory not found: {self.rules_dir}")
            return []
            
        for file_path in self.rules_dir.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Simple chunking by headers
                # This ensures we capture logical sections
                file_chunks = self._chunk_by_headers(content, file_path.name)
                chunks.extend(file_chunks)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        return chunks
        
    def _chunk_by_headers(self, content: str, filename: str) -> List[Dict[str, Any]]:
        """Split markdown content by headers"""
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_header = "Intro"
        
        for line in lines:
            if line.startswith('#'):
                # Save previous chunk if exists
                if current_chunk:
                    text = '\n'.join(current_chunk).strip()
                    if text:
                        chunks.append({
                            "source": filename,
                            "header": current_header,
                            "content": text
                        })
                
                # Start new chunk
                current_header = line.strip().lstrip('#').strip()
                current_chunk = [line]  # Include header in content
            else:
                current_chunk.append(line)
                
        # Save last chunk
        if current_chunk:
            text = '\n'.join(current_chunk).strip()
            if text:
                chunks.append({
                    "source": filename,
                    "header": current_header,
                    "content": text
                })
                
        return chunks

class SimpleVectorStore:
    """Lightweight in-memory vector store using numpy"""
    
    def __init__(self):
        self.vectors = []
        self.documents = []
        
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Add documents and their embeddings"""
        if not documents:
            return
            
        self.documents.extend(documents)
        
        # Convert to numpy array for efficiency if possible, or keep list
        if not self.vectors:
            self.vectors = np.array(embeddings)
        else:
            self.vectors = np.vstack((self.vectors, np.array(embeddings)))
            
    def search(self, query_embedding: List[float], k: int = 3) -> List[Dict[str, Any]]:
        """Find top-k similar documents using cosine similarity"""
        if len(self.vectors) == 0:
            return []
            
        query_vec = np.array(query_embedding)
        
        # Calculate cosine similarity
        # localized norm calculation to avoid devision by zero
        norm_vectors = np.linalg.norm(self.vectors, axis=1)
        norm_query = np.linalg.norm(query_vec)
        
        if norm_query == 0:
            return []
            
        similarities = np.dot(self.vectors, query_vec) / (norm_vectors * norm_query)
        
        # Get top k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            results.append({
                "document": self.documents[idx],
                "score": float(similarities[idx])
            })
            
        return results

class RAGManager:
    """Manages RAG operations"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RAGManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.llm_client = get_embedding_client() # Use dedicated embedding client
        self.vector_store = SimpleVectorStore()
        self.loader = RuleLoader()
        self._initialize_knowledge_base()
        self._initialized = True
        
    def _initialize_knowledge_base(self):
        """Load rules and build index"""
        print("Initializing RAG Knowledge Base...")
        chunks = self.loader.load_rules()
        
        if not chunks:
            print("No rules found to index.")
            return
            
        print(f"Found {len(chunks)} chunks. Generating embeddings...")
        embeddings = []
        
        # Batch processing could be added here if needed
        for chunk in chunks:
            try:
                # Embed content
                embedding = self.llm_client.embed(chunk["content"])
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error embedding chunk {chunk['header']}: {e}")
                # Use zero vector or skip? skipping for now to avoid dimension mismatch
                # Actually if embed fails, we can't search.
                # Let's clean up logic: only add successful embeddings
                pass
        
        # Filter chunks that correspond to successful embeddings
        # This is a bit naive, realistically we should match index
        # Let's redo to ensure alignment
        
        valid_chunks = []
        valid_embeddings = []
        
        for chunk in chunks:
            try:
                embedding = self.llm_client.embed(chunk["content"])
                valid_chunks.append(chunk)
                valid_embeddings.append(embedding)
            except Exception as e:
                print(f"Failed to embed chunk in {chunk['source']}: {e}")
                
        if valid_chunks:
            self.vector_store.add_documents(valid_chunks, valid_embeddings)
            print(f"RAG Knowledge Base initialized with {len(valid_chunks)} chunks.")
            
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant rules"""
        try:
            query_embedding = self.llm_client.embed(query)
            return self.vector_store.search(query_embedding, k=k)
        except Exception as e:
            print(f"Search failed: {e}")
            return []
            
    def get_suggested_topics(self, limit: int = 5) -> List[str]:
        """Get random topics (headers) from loaded rules"""
        import random
        
        all_docs = self.vector_store.documents
        if not all_docs:
            return []
            
        # Extract unique headers
        headers = list(set(doc['header'] for doc in all_docs if doc['header'] != 'Intro'))
        
        if not headers:
            return []
            
        # Shuffle and return top k
        random.shuffle(headers)
        return headers[:limit]
