import logging

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .. import config


logger = logging.getLogger(__name__)


def extract_text(file) -> str:
    """Extract text from an uploaded TXT file."""
    try:
        content = file.getvalue()
        decoded_text = content.decode("utf-8")

        logger.info(
            f"Extracted text from {file.name} successfully"
        )

        return decoded_text

    except UnicodeDecodeError as e:
        logger.error(
            f"Error extracting text from {file.name}: {e}"
        )
        raise


def chunk_text(text: str, chunk_size: int = 500) -> list:
    """Split text into smaller overlapping chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size // 10,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    logger.info(
        f"Text chunked into {len(chunks)} pieces "
        f"of size {chunk_size}"
    )

    return chunks


def embed_text(chunks: list) -> list:
    """Generate embeddings for each text chunk."""

    embedding_model = OllamaEmbeddings(
        model=config.EMBEDDING_MODEL_NAME
    )

    embeddings = embedding_model.embed_documents(chunks)

    logger.info(
        f"Generated embeddings for {len(chunks)} chunks"
    )

    return embeddings


def process_document(file):
    """Process an uploaded document through extraction, chunking, and embedding."""
    try:
        extracted_text = extract_text(file)
        chunks = chunk_text(extracted_text)
        embeddings = embed_text(chunks)

        logger.info(f"Document processed successfully: {file.name}")

        return extracted_text, chunks, embeddings

    except Exception as e:
        logger.error(f"Error processing document {file.name}: {e}")
        raise