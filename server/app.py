# app.py

# Import necessary modules
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Routes
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.serialize() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    if 'body' not in data or 'username' not in data:
        return jsonify({'error': 'Missing body or username'}), 400
    message = Message(body=data['body'], username=data['username'])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.serialize()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    data = request.json
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return jsonify(message.serialize())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'}), 200

if __name__ == '__main__':
    app.run(port=5555)
