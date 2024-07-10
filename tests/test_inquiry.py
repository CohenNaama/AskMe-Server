import os
import pytest
from unittest.mock import patch
from app import create_app, db


@pytest.fixture
def app():
    """
       Fixture to set up the Flask application for testing.

       Yields:
           Flask: The Flask application instance.
       """
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['OPENAI_API_KEY'] = 'sk-test-API-key'

    app = create_app()
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """
      Fixture to set up the Flask test client.

      Args:
          app (Flask): The Flask application instance.

      Returns:
          FlaskClient: The Flask test client.
      """
    return app.test_client()


def test_ask_endpoint(client):
    """
       Test the /ask endpoint with a valid question.

       Args:
           client (FlaskClient): The Flask test client.
       """
    mock_response = {
        'choices': [{'message': {'content': 'This is a mocked response.'}}]
    }
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with patch('app.db.session.add'), patch('app.db.session.commit'):
            response = client.post('/ask', json={'question': 'What is the capital of Israel?'})

            assert response.status_code == 201

            response_data = response.get_json()
            print("response_data:", response_data)
            assert response_data['question'] == 'What is the capital of Israel?'
            assert response_data['answer'] == 'This is a mocked response.'


def test_ask_endpoint_invalid_json(client):
    """
      Test the /ask endpoint with invalid JSON data.

      Args:
          client (FlaskClient): The Flask test client.
      """
    response = client.post('/ask', json={'wrong_key': 'What is the capital of Israel?'})
    assert response.status_code == 400
    response_data = response.get_json()
    print("response_data:", response_data)
    assert 'message' in response_data
    assert response_data['message'] == "Error: Invalid JSON data"
    assert 'details' in response_data


def test_ask_endpoint_empty_question(client):
    """
       Test the /ask endpoint with an empty question.

       Args:
           client (FlaskClient): The Flask test client.
       """
    response = client.post('/ask', json={'question': ''})
    assert response.status_code == 400
    response_data = response.get_json()
    print("response_data:", response_data)
    assert 'message' in response_data
    assert response_data['message'] == "Error: Invalid JSON data"
    assert 'details' in response_data
    assert response_data['details'] == "Question cannot be empty."

