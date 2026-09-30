import logging

logger = logging.getLogger(__name__)

def extract_text(file) -> str:
    """Extract text from an uploaded TXT file."""
    try:
        content = file.getvalue()
        decoded_text = content.decode("utf-8")
        logger.info(f"Extracted text from {file.name} successfully")
        return decoded_text
    except UnicodeDecodeError as e:
        logger.error(f"Error extracting text from {file.name}: {e}")
        raise