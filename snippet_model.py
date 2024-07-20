from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()

class Snippet(db.Model):
    __tablename__ = 'snippets'
  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Snippet {self.title}>'

try:
    db_uri = os.getenv("DATABASE_URL")
    if db_uri:
        if db_uri.startswith("postgres://"):
            db_uri = db_uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    else:
        raise ValueError("DATABASE_URL is not defined in .env file.")
except ValueError as e:
    print(e)  # Log the error appropriately for your set-up
    # You might want to exit the app or handle this in a way that informs the user/admin.
except Exception as e:
    print(f"An error occurred: {e}")  # General catch-all for unexpected errors

try:
    db.init_app(app)
except Exception as e:
    print(f"An error occurred during SQLAlchemy initialization: {e}")
    # Handle or log the initialization failure accordingly