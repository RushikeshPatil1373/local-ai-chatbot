import logging

import pymupdf
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .. import config


logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".txt", ".pdf"}


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


def extract_pdf_text(file) -> str:
    """Extract text from an uploaded PDF file.

    Uses PyMuPDF to read every page and concatenate the text.
    Raises ``ValueError`` if the PDF contains no extractable text
    (e.g. scanned images without OCR).
    """
    try:
        pdf_bytes = file.getvalue()
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

        pages_text: list[str] = []
        for page_number, page in enumerate(doc, start=1):
            page_text = page.get_text()
            if page_text.strip():
                pages_text.append(page_text)

        doc.close()

        if not pages_text:
            raise ValueError(
                f"No extractable text found in '{file.name}'. "
                "The PDF may contain only scanned images."
            )

        full_text = "\n\n".join(pages_text)

        logger.info(
            f"Extracted text from PDF '{file.name}' – "
            f"{len(pages_text)} page(s), {len(full_text)} characters"
        )

        return full_text

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error extracting text from PDF '{file.name}': {e}")
        raise ValueError(
            f"Could not read '{file.name}' as a valid PDF: {e}"
        ) from e


def _get_file_extension(filename: str) -> str:
    """Return the lowercased file extension (e.g. '.pdf')."""
    dot_index = filename.rfind(".")
    if dot_index == -1:
        return ""
    return filename[dot_index:].lower()


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
    """Process an uploaded document through extraction, chunking, and embedding.

    Supports .txt and .pdf files. Raises ``ValueError`` for unsupported types.
    """
    ext = _get_file_extension(file.name)

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    try:
        if ext == ".pdf":
            extracted_text = extract_pdf_text(file)
        else:
            extracted_text = extract_text(file)

        chunks = chunk_text(extracted_text)
        embeddings = embed_text(chunks)

        logger.info(f"Document processed successfully: {file.name}")

        return extracted_text, chunks, embeddings

    except Exception as e:
        logger.error(f"Error processing document {file.name}: {e}")
        raise