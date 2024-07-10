import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
      Configuration class for the Flask application.

      Attributes:
          SECRET_KEY (str): The secret key for the application.
          SQLALCHEMY_DATABASE_URI (str): The database URI for SQLAlchemy.
          SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable SQLAlchemy event system.
          OPENAI_API_KEY (str): The API key for OpenAI.
      """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
