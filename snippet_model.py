from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask import Flask, jsonify

# Load environment variables
load_dotenv()

# Initialize Flask app and SQLAlchemy ORM
app = Flask(__name__)
database = SQLAlchemy()

class CodeSnippet(database.Model):
    __tablename__ = 'code_snippets'
  
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    code_content = database.Column(database.Text, nullable=False)
    programming_language = database.Column(database.String(50), nullable=False)
    description = database.Column(database.Text)
    creator_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<CodeSnippet {self.title}>'

try:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Ensure compatibility with PostgreSQL URLs
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        # Configure database connection
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        raise ValueError("DATABASE_URL is not defined in the .env file.")
except ValueError as error:
    print(error)  # Log the error appropriately for your set-up
except Exception as general_error:
    print(f"An unexpected error occurred: {general_error}")  # General catch-all for unexpected errors

try:
    # Initialize SQLAlchemy with Flask app
    database.init_app(app)
except Exception as init_error:
    print(f"An error occurred during SQLAlchemy initialization: {init_error}")