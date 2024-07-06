from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database Configuration
DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLIALIZED_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

# Ensure JSON Requests
@app.before_request
def ensure_json_request():
    if request.is_json:
        request.json_data = request.get_json()

# Models
class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)

class CodeSnippet(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    code = database.Column(database.Text, nullable=False)
    author_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    author = database.relationship('User', backref=database.backref('code_snippets', lazy=True))

# Create database tables before first request
@app.before_first_request
def initialize_database():
    database.create_all()

# User functionality
def add_user_to_database(username):
    user_instance = User(username=username)
    database.session.add(user_instance)
    database.session.commit()
    return user_instance

# Snippet functionality
def add_snippet_to_database(code, author_id):
    snippet_instance = CodeSnippet(code=code, author_id=author_id)
    database.session.add(snippet_instance)
    database.session.commit()
    return snippet_instance

def format_code_snippets(snippets):
    return [{'id': snippet.id, 'code': snippet.code} for snippet in snippets]

# Routes
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the CodeSnippetHub!'})

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json_data['username']
    add_user_to_database(username)
    return jsonify({'message': 'User successfully added.'}), 201

@app.route('/snippets', methods=['POST'])
def add_snippet():
    code = request.json_data['code']
    author_id = request.json_data['user_id']
    add_snippet_to_database(code, author_id)
    return jsonify({'message': 'Code snippet successfully added.'}), 201

@app.route('/snippets', methods=['GET'])
def fetch_snippets():
    all_snippets = CodeSnippet.query.all()
    serialized_snippets = format_code_snippets(all_snippets)
    return jsonify({'snippets': serialized_snippets})

@app.route('/users/<int:user_id>/snippets', methods=['GET'])
def fetch_user_snippets(user_id):
    user_with_snippets = User.query.get_or_404(user_id)
    formatted_snippets = format_code_snippets(user_with_snippets.code_snippets)
    return jsonify({'snippets': formatted_snippets})

if __name__ == '__main__':
    app.run(port=5000, debug=True)