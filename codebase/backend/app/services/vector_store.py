from typing import Any, Dict, List, Optional
from app.core.chroma import get_chroma_client, get_chroma_collection
from app.core.config import settings
from app.schemas.vector_store import (
    AddDocumentsRequest,
    AddDocumentsResponse,
    CollectionInfo,
    CollectionListResponse,
    QueryRequest,
    QueryResponse,
    QueryResultItem,
    VectorStoreHealthResponse,
)


class VectorStoreService:
    @staticmethod
    def health_check() -> VectorStoreHealthResponse:
        client = get_chroma_client()
        collections = client.list_collections()
        mode = "remote" if settings.CHROMA_HOST else "persistent"
        return VectorStoreHealthResponse(
            status="ok",
            mode=mode,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY if mode == "persistent" else None,
            collections_count=len(collections)
        )

    @staticmethod
    def add_documents(request: AddDocumentsRequest) -> AddDocumentsResponse:
        collection = get_chroma_collection(request.collection_name)
        
        ids = [doc.id for doc in request.documents]
        documents = [doc.content for doc in request.documents]
        metadatas = [doc.metadata or {} for doc in request.documents]

        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        return AddDocumentsResponse(
            status="success",
            added_count=len(ids),
            collection_name=collection.name
        )

    @staticmethod
    def query(request: QueryRequest) -> QueryResponse:
        collection = get_chroma_collection(request.collection_name)
        
        kwargs: Dict[str, Any] = {
            "query_texts": request.query_texts,
            "n_results": request.n_results,
        }
        if request.where:
            kwargs["where"] = request.where

        raw_results = collection.query(**kwargs)

        formatted_results: List[List[QueryResultItem]] = []
        
        if raw_results and "ids" in raw_results:
            batch_count = len(raw_results["ids"])
            for b in range(batch_count):
                batch_items: List[QueryResultItem] = []
                ids = raw_results["ids"][b]
                docs = raw_results["documents"][b] if raw_results.get("documents") else [""] * len(ids)
                metas = raw_results["metadatas"][b] if raw_results.get("metadatas") else [{}] * len(ids)
                dists = raw_results["distances"][b] if raw_results.get("distances") else [None] * len(ids)

                for idx in range(len(ids)):
                    batch_items.append(
                        QueryResultItem(
                            id=ids[idx],
                            document=docs[idx],
                            metadata=metas[idx],
                            distance=dists[idx]
                        )
                    )
                formatted_results.append(batch_items)

        return QueryResponse(
            collection_name=collection.name,
            results=formatted_results
        )

    @staticmethod
    def list_collections() -> CollectionListResponse:
        client = get_chroma_client()
        collections = client.list_collections()
        
        info_list: List[CollectionInfo] = []
        for col in collections:
            info_list.append(
                CollectionInfo(
                    name=col.name,
                    count=col.count()
                )
            )
        return CollectionListResponse(collections=info_list)

    @staticmethod
    def delete_collection(name: str) -> bool:
        client = get_chroma_client()
        client.delete_collection(name=name)
        return True
