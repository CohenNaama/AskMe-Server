from app.models.inquiry import Inquiry
from app import db


def create_inquiry(question, answer=None):
    """
       Create a new inquiry.

       Args:
           question (str): The question to be asked.
           answer (str, optional): The answer to the question. Defaults to None.

       Returns:
           Inquiry: The created inquiry instance.
       """
    new_inquiry = Inquiry(question=question, answer=answer)
    db.session.add(new_inquiry)
    db.session.commit()
    return new_inquiry


def get_all_inquiries():
    """
       Retrieve all inquiries.

       Returns:
           list: A list of all inquiries.
       """
    return Inquiry.query.all()


def get_inquiry_by_id(inquiry_id):
    """
       Retrieve an inquiry by its ID.

       Args:
           inquiry_id (int): The ID of the inquiry.

       Returns:
           Inquiry: The inquiry instance with the specified ID.
       """
    return Inquiry.query.get(inquiry_id)
