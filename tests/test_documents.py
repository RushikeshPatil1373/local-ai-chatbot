import pytest
import pymupdf

from src.chatbot.documents import (
    chunk_text,
    extract_pdf_text,
    extract_text,
    process_document,
    _get_file_extension,
    SUPPORTED_EXTENSIONS,
)


class UploadedFile:
    """Minimal stub that mimics a Streamlit UploadedFile."""

    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content

    def getvalue(self):
        return self.content


def _make_pdf_bytes(text: str, num_pages: int = 1) -> bytes:
    """Create a real in-memory PDF with *text* on *num_pages* pages."""
    doc = pymupdf.open()
    for i in range(num_pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"{text} (page {i + 1})")
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


# ── extract_text (TXT) ──────────────────────────────────────────────

def test_extract_text_decodes_utf8_file():
    uploaded_file = UploadedFile("notes.txt", "Hello, world!".encode("utf-8"))

    assert extract_text(uploaded_file) == "Hello, world!"


def test_extract_text_rejects_invalid_utf8_file():
    uploaded_file = UploadedFile("bad.txt", b"invalid\xfftext")

    with pytest.raises(UnicodeDecodeError):
        extract_text(uploaded_file)


# ── extract_pdf_text ────────────────────────────────────────────────

def test_extract_pdf_text_reads_single_page():
    pdf_bytes = _make_pdf_bytes("Hello from PDF")
    uploaded_file = UploadedFile("doc.pdf", pdf_bytes)

    text = extract_pdf_text(uploaded_file)

    assert "Hello from PDF" in text


def test_extract_pdf_text_reads_multiple_pages():
    pdf_bytes = _make_pdf_bytes("Multi-page content", num_pages=3)
    uploaded_file = UploadedFile("multi.pdf", pdf_bytes)

    text = extract_pdf_text(uploaded_file)

    assert "page 1" in text
    assert "page 3" in text


def test_extract_pdf_text_rejects_empty_pdf():
    # An empty PDF (no text on the page)
    doc = pymupdf.open()
    doc.new_page()  # blank page
    pdf_bytes = doc.tobytes()
    doc.close()

    uploaded_file = UploadedFile("empty.pdf", pdf_bytes)

    with pytest.raises(ValueError, match="No extractable text"):
        extract_pdf_text(uploaded_file)


def test_extract_pdf_text_rejects_invalid_bytes():
    uploaded_file = UploadedFile("corrupt.pdf", b"this is not a pdf")

    with pytest.raises(ValueError, match="Could not read"):
        extract_pdf_text(uploaded_file)


# ── _get_file_extension ────────────────────────────────────────────

def test_get_file_extension_pdf():
    assert _get_file_extension("report.pdf") == ".pdf"


def test_get_file_extension_txt():
    assert _get_file_extension("notes.txt") == ".txt"


def test_get_file_extension_uppercase():
    assert _get_file_extension("FILE.PDF") == ".pdf"


def test_get_file_extension_no_extension():
    assert _get_file_extension("README") == ""


# ── process_document routing ───────────────────────────────────────

def test_process_document_rejects_unsupported_extension():
    uploaded_file = UploadedFile("image.png", b"fake-png-data")

    with pytest.raises(ValueError, match="Unsupported file type"):
        process_document(uploaded_file)


# ── chunk_text ──────────────────────────────────────────────────────

def test_chunk_text_creates_multiple_chunks():
    text = "This is a test sentence. " * 50

    chunks = chunk_text(text, chunk_size=100)

    assert isinstance(chunks, list)
    assert len(chunks) > 1


def test_chunk_text_preserves_content():
    text = "First paragraph.\n\nSecond paragraph."

    chunks = chunk_text(text, chunk_size=100)

    assert "First paragraph." in chunks[0]
    assert "Second paragraph." in chunks[0]


def test_chunk_text_handles_empty_text():
    assert chunk_text("") == []


def test_chunk_text_rejects_non_positive_chunk_size():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("text", chunk_size=0)