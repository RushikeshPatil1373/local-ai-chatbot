from src.chatbot import vectorstore


class FakeCollection:
    def __init__(self):
        self.add_calls = []

    def add(self, **values):
        self.add_calls.append(values)

    def query(self, **values):
        self.query_values = values
        return {"documents": [["matching chunk"]]}


class FakeClient:
    def __init__(self, collection):
        self.collection = collection

    def get_or_create_collection(self, name):
        assert name == "document_embeddings"
        return self.collection


class FakeEmbeddings:
    def __init__(self, model):
        self.model = model

    def embed_query(self, question):
        assert question == "How does this work?"
        return [0.1, 0.2]


def test_store_embeddings_rejects_mismatched_inputs():
    try:
        vectorstore.store_embeddings(["one"], [])
    except ValueError as error:
        assert str(error) == "Chunks and embeddings must have the same length."
    else:
        raise AssertionError("store_embeddings should reject mismatched inputs")


def test_store_embeddings_writes_chunks_and_metadata(monkeypatch):
    collection = FakeCollection()
    monkeypatch.setattr(
        vectorstore.chromadb,
        "PersistentClient",
        lambda path: FakeClient(collection),
    )

    document_id = vectorstore.store_embeddings(
        ["first", "second"],
        [[0.1], [0.2]],
    )

    values = collection.add_calls[0]
    assert document_id
    assert values["documents"] == ["first", "second"]
    assert values["embeddings"] == [[0.1], [0.2]]
    assert values["ids"] == [
        f"{document_id}__chunk_0",
        f"{document_id}__chunk_1",
    ]
    assert values["metadatas"] == [
        {"document_id": document_id, "chunk_index": 0},
        {"document_id": document_id, "chunk_index": 1},
    ]


def test_retrieve_chunks_embeds_question_and_returns_documents(monkeypatch):
    collection = FakeCollection()
    monkeypatch.setattr(
        vectorstore.chromadb,
        "PersistentClient",
        lambda path: FakeClient(collection),
    )
    monkeypatch.setattr(vectorstore, "OllamaEmbeddings", FakeEmbeddings)

    chunks = vectorstore.retrieve_chunks("How does this work?", n_results=2)

    assert chunks == ["matching chunk"]
    assert collection.query_values == {
        "query_embeddings": [[0.1, 0.2]],
        "n_results": 2,
    }


def test_retrieve_chunks_rejects_non_positive_result_count():
    try:
        vectorstore.retrieve_chunks("question", n_results=0)
    except ValueError as error:
        assert str(error) == "n_results must be greater than zero."
    else:
        raise AssertionError("retrieve_chunks should reject non-positive result counts")