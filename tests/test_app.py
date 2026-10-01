from streamlit.testing.v1 import AppTest


def test_streamlit_app_starts_without_external_services():
    app = AppTest.from_file("app.py").run()

    assert not app.exception
    assert app.title[0].value == "Local AI Chatbot"