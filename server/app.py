from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()

    if not messages:
        return jsonify({'error': 'Message not found'}), 404
    
    arr_messages = []
    for message in messages:
        message_obj = {
            'id': message.id,
            'body': message.body,
            'username': message.username,               
            'created_at': message.created_at, 
            'updated_at': message.updated_at, 
        }
        arr_messages.append(message_obj)

    return jsonify(arr_messages), 200


@app.route('/createmessages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(id=data.get('id'),
                          body=data.get('body'), 
                          username=data.get('username'),
                          created_at=datetime.utcnow(),
                          updated_at=datetime.utcnow())
    db.session.add(new_message)
    db.session.commit()

    response_data = {
        'message': 'Message created successfully'
    }
    return jsonify(response_data)


@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    # Get the restaurant by ID
    message = Message.query.get(id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404

  

    # Create restaurant object with pizzas included
    message_obj = {
        'id': message.id,
        'body': message.body,
        'username': message.username
    }


    return jsonify(message_obj), 200

if __name__ == '__main__':
    app.run(port=5555)
