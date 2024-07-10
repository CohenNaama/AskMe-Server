import openai
from app.models.inquiry import Inquiry
from app import db
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


def create_inquiry(question, openai_client=openai):
    """
       Create a new inquiry and get the answer from OpenAI.

       Args:
           question (str): The question to be asked.
           openai_client (module): The OpenAI client module. Defaults to openai.

       Returns:
           Inquiry: The created inquiry instance.

       Raises:
           ValueError: If the question is empty.
       """
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
