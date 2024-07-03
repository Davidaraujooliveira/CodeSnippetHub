from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mydatabase.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.before_request
def before_request():
    if request.is_json:
        request.data = request.get_json()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_path=True)
    code = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('snippets', lazy=True))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Snippet Manager!'})

@app.route('/users', methods=['POST'])
def create_user():
    username = request.data['username']
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201

@app.route('/snippets', methods=['POST'])
def create_snippet():
    code = request.data['code']
    user_id = request.data['user_id']
    new_snippet = Snippet(code=code, user_id=user_id)
    db.session.add(new_snippet)
    db.session.commit()
    return jsonify({'message': 'Snippet created successfully.'}), 201

@app.route('/snippets', methods=['GET'])
def get_snippets():
    snippets = Snippet.query.all()
    return jsonify({'snippets': [{'id': snippet.id, 'code': snippet.code} for snippet in snippets]})

@app.route('/users/<int:user_id>/snippets', methods=['GET'])
def get_user_snippets(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'snippets': [{'id': snippet.id, 'code': snippet.code} for snippet in user.snippets]})

if __name__ == '__main__':
    app.run(port=5000, debug=True)