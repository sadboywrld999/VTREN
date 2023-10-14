import os
from flask import Flask, render_template
import socketio
from googletrans import Translator  # Use the Google Translate library for language translation

# Initialize Flask and Socket.IO
app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins='*')

# Initialize the language translator
translator = Translator()

# Dictionary to store user preferences (username: preferred_language)
user_preferences = {}

# Web interface for messaging
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket connection
@sio.on('connect')
def connect(sid, environ):
    print(f'User {sid} connected')

# WebSocket event for user registration
@sio.on('register')
def register_user(sid, data):
    username = data['username']
    preferred_language = data['preferred_language']
    user_preferences[sid] = preferred_language
    print(f'User {sid} registered as {username} with preferred language {preferred_language}')

# WebSocket message handling
@sio.on('send_message')
def handle_message(sid, data):
    message = data['message']
    source_language = detect_language(message)
    preferred_language = user_preferences[sid]

    # Translate the message to the user's preferred language
    translated_message = translate_message(message, source_language, preferred_language)

    # Send the translated message to the recipient
    sio.emit('receive_message', {'username': get_username(sid), 'message': translated_message}, room=sid)

# WebSocket disconnection
@sio.on('disconnect')
def disconnect(sid):
    user_preferences.pop(sid, None)
    print(f'User {sid} disconnected')

def detect_language(text):
    # Implement your language detection logic here
    # For simplicity, you can use a language detection library like langdetect

def translate_message(message, source_language, preferred_language):
    # Implement the translation logic here using the Google Translate library
    translation = translator.translate(message, src=source_language, dest=preferred_language)
    return translation.text

def get_username(sid):
    # Retrieve the username associated with the WebSocket session (from a database or memory store)
    # For simplicity, you can store usernames in a dictionary (sid: username)
    
if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
