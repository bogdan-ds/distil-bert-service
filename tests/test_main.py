from unittest.mock import patch

from fastapi.testclient import TestClient
from src.main import app

from tests.mocks import mocked_entities


@patch("src.main.run_nlp_pipeline")
def test_ner_endpoint(mock_run_nlp_pipeline):
    mock_run_nlp_pipeline.return_value = mocked_entities
    sample_request_payload = {"text": "Just some text"}
    with TestClient(app) as client:
        response = client.post("/ner", json=sample_request_payload)
    assert response.status_code == 200
    assert response.json()["text"] == "Just some text"
    assert response.json()["entities"] == mocked_entities


@patch("src.main.run_nlp_pipeline")
def test_ner_endpoint_invalid_input(mock_run_nlp_pipeline):
    mock_run_nlp_pipeline.return_value = mocked_entities
    with TestClient(app) as client:
        response = client.post("/ner", json={"text": ""})
    assert response.status_code == 422
