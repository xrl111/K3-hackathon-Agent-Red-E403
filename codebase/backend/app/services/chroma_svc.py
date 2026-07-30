import uuid
import random
from app.core.chroma import get_chroma_client
from app.schemas.rag import RagInjectRequest, RagInjectResponse

class ChromaService:
    @staticmethod
    def inject_documents(assessment_id: str, request: RagInjectRequest) -> RagInjectResponse:
        """
        Creates a new ChromaDB collection, chunks the input texts, simulates poisoned chunks,
        and saves them to ChromaDB.
        """
        client = get_chroma_client()
        collection_name = f"rag_sandbox_{assessment_id}"
        
        # Get or create collection
        collection = client.get_or_create_collection(name=collection_name)
        
        chunk_size = request.chunk_size
        poison_ratio = request.poison_ratio
        
        chunks = []
        
        # Simple text chunking
        for text in request.texts:
            # A simplistic chunking strategy: split into parts of length `chunk_size`
            # In a real app, you might use recursive character text splitters (e.g. from LangChain)
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                chunks.append(chunk)
                
        total_chunks = len(chunks)
        poisoned_chunks_count = 0
        
        ids = []
        documents = []
        metadatas = []
        
        for idx, chunk in enumerate(chunks):
            chunk_id = f"chunk_{uuid.uuid4()}"
            is_poisoned = False
            
            # Simulate poisoned chunk
            if random.random() < poison_ratio:
                is_poisoned = True
                poisoned_chunks_count += 1
                
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({"is_poisoned": is_poisoned, "assessment_id": assessment_id, "chunk_index": idx})
            
        if ids:
            # Insert into ChromaDB collection
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
        return RagInjectResponse(
            message="Injected successfully to ChromaDB",
            total_chunks=total_chunks,
            poisoned_chunks=poisoned_chunks_count,
            collection_name=collection_name
        )
