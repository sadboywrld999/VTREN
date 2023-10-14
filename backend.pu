from flask import Flask, request, jsonify
from googletrans import Translator  # Use the Google Translate library for language translation
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for your API

# Configure your database (e.g., PostgreSQL, MySQL, SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

# Initialize the language translator
translator = Translator()

# Define a Message model for the database
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    recipient = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    source_language = db.Column(db.String(10), nullable=False)
    translated_message = db.Column(db.String(500), nullable=False)

# API route for sending and receiving messages
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']

    # Detect source language and translate the message
    source_language = detect_language(message)
    translated_message = translate_message(message, source_language, recipient)

    # Store the original and translated message in the database
    new_message = Message(sender=sender, recipient=recipient, message=message,
                          source_language=source_language, translated_message=translated_message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully"})

# API route for fetching messages
@app.route('/get_messages/<user>', methods=['GET'])
def get_messages(user):
    messages = Message.query.filter_by(recipient=user).all()
    message_list = [{'sender': message.sender, 'message': message.message,
                     'translated_message': message.translated_message} for message in messages]
    return jsonify(message_list)

def detect_language(text):
    # Implement your language detection logic here
    # For simplicity, you can use a language detection library like langdetect

def translate_message(message, source_language, recipient):
    if recipient != 'preferred_language':
        # Translate the message to the recipient's preferred language
        translation = translator.translate(message, src=source_language, dest=recipient)
        return translation.text
    else:
        # If the recipient prefers the source language, return the original message
        return message

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
