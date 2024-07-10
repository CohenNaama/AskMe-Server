from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from app import db


class Inquiry(db.Model, SerializerMixin):
    """
       Model representing an inquiry.

       Attributes:
           id (int): The primary key for the inquiry.
           question (str): The question asked.
           answer (str): The answer provided by the AI.
           created_at (datetime): The timestamp when the inquiry was created.
       """
    __tablename__ = 'inquiries'
    serialize_only = ('id', 'question', 'answer', 'created_at')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(500), nullable=False, index=True)
    answer = db.Column(db.String(500), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        """
              Convert the inquiry instance to a dictionary.

              Returns:
                  dict: A dictionary representation of the inquiry.
              """
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at,
        }

    def __repr__(self):
        """
               Return a string representation of the inquiry.

               Returns:
                   str: A string representation of the inquiry.
               """
        return f'<Inquiry {self.id} - {self.question[:20]}>'
