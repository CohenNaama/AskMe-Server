from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from app import db


class Inquiry(db.Model, SerializerMixin):
    __tablename__ = 'inquiries'
    serialize_only = ('id', 'question', 'answer', 'created_at')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(500), nullable=False, index=True)
    answer = db.Column(db.String(500), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at,
        }

    def __repr__(self):
        return f'<Inquiry {self.id} - {self.question[:20]}>'
