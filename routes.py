from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('snippets', lazy=True))

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    if username:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'username': new_user.username}), 201
    return jsonify({'message': 'Username is required'}), 400

@api_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.username = request.json.get('username', user.username)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username})

@api_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@api_blueprint.route('/snippets', methods=['POST'])
def create_snippet():
    code, user_id = request.json.get('code'), request.json.get('user_id')
    if code and user_id:
        new_snippet = Snippet(code=code, user_id=user_id)
        db.session.add(new_snippet)
        db.session.commit()
        return jsonify({'id': new_snippet.id, 'code': new_snippet.code, 'user_id': new_snippet.user_id}), 201
    return jsonify({'message': 'Code and User ID are required'}), 400

@api_blueprint.route('/snippets/<int:id>', methods=['PUT'])
def update_snippet(id):
    snippet = Snippet.query.get(id)
    if not snippet:
        return jsonify({'message': 'Snippet not found'}), 404
    snippet.code = request.json.get('code', snippet.code)
    db.session.commit()
    return jsonify({'id': snippet.id, 'represent': snippet.code})

@api_blueprint.route('/snippets/<int:id>', methods=['DELETE'])
def delete_snippet(id):
    snippet = Snippet.query.get(id)
    if not snippet:
        return jsonify({'message': 'Snippet not found'}), 404
    db.session.delete(snippet)
    db.session.commit()
    return jsonify({'message': 'Snippet deleted'})

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)