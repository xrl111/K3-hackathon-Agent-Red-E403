import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from app.core.config import settings

_chroma_client = None
_embedding_function = None


def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.HF_EMBEDDING_MODEL
        )
    return _embedding_function


def get_chroma_client() -> chromadb.ClientAPI:
    """
    Khởi tạo Persistent Client kết nối tới ChromaDB lưu tại CHROMA_PATH.
    """
    global _chroma_client
    if _chroma_client is None:
        if settings.CHROMA_HOST:
            _chroma_client = chromadb.HttpClient(
                host=settings.CHROMA_HOST,
                port=settings.CHROMA_PORT
            )
        else:
            _chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PATH,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
    return _chroma_client


def get_chroma_collection(name: str = None) -> chromadb.Collection:
    """
    Get or create a ChromaDB collection by name.
    If name is not specified, uses CHROMA_DEFAULT_COLLECTION from config.
    """
    client = get_chroma_client()
    collection_name = name or settings.CHROMA_DEFAULT_COLLECTION
    emb_fn = get_embedding_function()
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=emb_fn
    )

