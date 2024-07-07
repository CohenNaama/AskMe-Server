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
    try:
        data = request.json
        inquiry = create_inquiry(data['question'])
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
    return render_template('index.html')
