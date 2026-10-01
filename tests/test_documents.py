import pytest

from src.chatbot.documents import chunk_text, extract_text


class UploadedFile:
    name = "notes.txt"

    def __init__(self, content: bytes):
        self.content = content

    def getvalue(self):
        return self.content


def test_extract_text_decodes_utf8_file():
    uploaded_file = UploadedFile("Hello, world!".encode("utf-8"))

    assert extract_text(uploaded_file) == "Hello, world!"


def test_extract_text_rejects_invalid_utf8_file():
    uploaded_file = UploadedFile(b"invalid\xfftext")

    with pytest.raises(UnicodeDecodeError):
        extract_text(uploaded_file)


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