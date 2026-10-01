import logging
import uuid
import chromadb
from .. import config
from langchain_ollama import OllamaEmbeddings

logger = logging.getLogger(__name__)

def store_embeddings(chunks: list, embeddings: list):
    """Store document chunks and their embeddings in ChromaDB."""
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have the same length.")

    try:
        document_id = str(uuid.uuid4())
        client = chromadb.PersistentClient(path=config.CHROMA_PATH)
        collection = client.get_or_create_collection(name="document_embeddings")
        ids = [f"{document_id}__chunk_{i}" for i in range(len(chunks))]
        metadata = [
            {   
                "document_id": document_id, 
                "chunk_index": i
            } for i in range(len(chunks))
            ]
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )
        logger.info(f"Stored {len(chunks)} chunks and embeddings in ChromaDB with document_id: {document_id}")

        return document_id
    except Exception as e:
        logger.error(f"Error storing embeddings in ChromaDB: {e}")
        raise

def retrieve_chunks(question: str, n_results: int = 3) -> list:
    """Retrieve the most relevant document chunks for a question."""
    if n_results <= 0:
        raise ValueError("n_results must be greater than zero.")

    try:
        embedding_model = OllamaEmbeddings(model=config.EMBEDDING_MODEL_NAME)
        question_embedding = embedding_model.embed_query(question)
        client = chromadb.PersistentClient(path=config.CHROMA_PATH)
        collection = client.get_or_create_collection(name="document_embeddings")
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=n_results
        )
        return results.get("documents", [[]])[0]

    except Exception as e:
        logger.error(f"Error retrieving chunks from ChromaDB: {e}")
        raise