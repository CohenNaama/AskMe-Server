import os
import openai
from flask import Blueprint, request, jsonify, render_template
from app.services.inquiry_service import create_inquiry
from app.schemas.inquiry_schema import inquiry_schema
from app.utils.json_validator import json_validator

main = Blueprint('main', __name__)

openai.api_key = os.getenv('OPENAI_API_KEY')


@main.route('/ask', methods=['POST'])
@json_validator(inquiry_schema)
def ask_question():
    """
        Handle the endpoint for asking a question.

        Validates the request JSON against the inquiry schema and processes the inquiry.

        Returns:
            Response: JSON response containing the inquiry details or an error message.
        """
    try:
        data = request.json
        inquiry = create_inquiry(data['question'])
    except ValueError as ve:
        return jsonify({'message': 'Error: Invalid JSON data', 'details': str(ve)}), 400
    except Exception as e:
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500

    result = {
        'id': inquiry.id,
        'question': inquiry.question,
        'answer': inquiry.answer,
        'created_at': inquiry.created_at
    }
    return jsonify(result), 201


@main.route('/')
def home():
    """
        Render the home page.

        Returns:
            Response: Rendered HTML template for the home page.
        """
    return render_template('index.html')
