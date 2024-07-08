# import openai
# from app.models.inquiry import Inquiry
# from app import db
# import os
#
#
# openai.api_key = os.getenv('OPENAI_API_KEY')
#
#
# def create_inquiry(question):
#     api_key = os.getenv('OPENAI_API_KEY')
#     openai.api_key = api_key
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": question},
#         ]
#     )
#     answer = response.choices[0].message['content'].strip()
#
#     new_inquiry = Inquiry(question=question, answer=answer)
#     db.session.add(new_inquiry)
#     db.session.commit()
#     return new_inquiry


# app/services/inquiry_service.py
import openai
from app.models.inquiry import Inquiry
from app import db
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


def create_inquiry(question, openai_client=openai):
    if not question.strip():
        raise ValueError("Question cannot be empty.")
    api_key = os.getenv('OPENAI_API_KEY')
    openai_client.api_key = api_key
    response = openai_client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ]
    )
    answer = response['choices'][0]['message']['content'].strip()

    new_inquiry = Inquiry(question=question, answer=answer)
    db.session.add(new_inquiry)
    db.session.commit()
    return new_inquiry
