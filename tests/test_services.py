import httpx
import pytest

from src.chatbot import services


class FakeResponse:
    content = "A test response"


class FakeChain:
    def __init__(self):
        self.calls = []

    def invoke(self, values):
        self.calls.append({**values, "history": list(values["history"])})
        return FakeResponse()


def make_service(monkeypatch):
    monkeypatch.setattr(services, "ChatOllama", lambda model: lambda values: None)
    service = services.ChatbotService()
    service.chain = FakeChain()
    return service


def test_ask_invokes_chain_and_records_exchange(monkeypatch):
    service = make_service(monkeypatch)

    response = service.ask("What is Python?", context="A programming language")

    assert response == "A test response"
    assert len(service.history) == 2
    assert service.history[0].content == "What is Python?"
    assert service.history[1].content == "A test response"
    assert service.chain.calls[0] == {
        "history": [],
        "context": "A programming language",
        "input": "What is Python?",
    }


def test_trim_history_keeps_latest_exchanges(monkeypatch):
    service = make_service(monkeypatch)

    for index in range(6):
        service.ask(f"Question {index}")

    assert len(service.history) == 10
    assert service.history[0].content == "Question 1"
    assert service.history[-1].content == "A test response"


def test_trim_history_rejects_negative_exchange_limit(monkeypatch):
    service = make_service(monkeypatch)

    with pytest.raises(ValueError, match="negative"):
        service.trim_history(-1)


def test_ask_reraises_connection_errors(monkeypatch):
    service = make_service(monkeypatch)
    error = httpx.ConnectError(
        "Ollama unavailable",
        request=httpx.Request("POST", "http://localhost"),
    )
    service.chain.invoke = lambda values: (_ for _ in ()).throw(error)

    with pytest.raises(httpx.ConnectError):
        service.ask("Hello")

    assert service.history == []