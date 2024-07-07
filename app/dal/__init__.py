from app.models.inquiry import Inquiry
from app import db


def create_inquiry(question, answer=None):
    new_inquiry = Inquiry(question=question, answer=answer)
    db.session.add(new_inquiry)
    db.session.commit()
    return new_inquiry


def get_all_inquiries():
    return Inquiry.query.all()


def get_inquiry_by_id(inquiry_id):
    return Inquiry.query.get(inquiry_id)
