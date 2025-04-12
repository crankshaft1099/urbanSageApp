from flask import Flask, render_template, request, jsonify, send_from_directory, session
import requests
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')
# Set a secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Change this to a secure secret key

# In-memory store for chat histories (in production, use a database)
chat_sessions = {}

class ChatSession:
    def __init__(self):
        self.messages = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    def add_message(self, role, content):
        self.messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        self.last_activity = datetime.now()

    def get_history(self):
        return self.messages

# Configuration
API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://api.example.com/chat')  # Replace with your actual API endpoint
API_KEY = os.getenv('API_KEY', 'your-api-key-here')  # Replace with your actual API key

def test_fun(message, session_id):
    """
    Makes a call to the external API with the user's message and session ID.
    Returns the API response or an error message if the call fails.
    """
    try:
        # Prepare the request headers and data
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        """
        data = {
            'query': message,
            'sessionId': session_id,  # Send session ID instead of history
            'timestamp': datetime.now().isoformat()
        }
        """

        data = {
            'query': message,
            'sessionId': session_id,  # Send session ID instead of history
            'timestamp': datetime.now().isoformat()
        }

        # Make the API call
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=data,
            timeout=100  # 10 second timeout
        )

        # Check if the request was successful
        response.raise_for_status()
        
        # Parse and return the response
        return response.json().get('finalResponse', 'No response from API')

    except requests.exceptions.Timeout:
        return "Sorry, the request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Sorry, there was an error connecting to the API: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@app.before_request
def before_request():
    # Create a new session ID if one doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Initialize chat session if it doesn't exist
    session_id = session['session_id']
    if session_id not in chat_sessions:
        chat_sessions[session_id] = ChatSession()

@app.route('/')
def home():
    # Get chat history for the current session
    session_id = session['session_id']
    chat_history = chat_sessions[session_id].get_history()
    return render_template('index.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    session_id = session['session_id']
    chat_session = chat_sessions[session_id]
    
    # Add user message to history
    chat_session.add_message('user', user_message)
    
    # Call the test function with session ID instead of history
    api_response = test_fun(user_message, session_id)
    
    # Add bot response to history
    chat_session.add_message('bot', api_response)
    
    return jsonify({
        'response': api_response,
        'session_id': session_id
    })

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear the current session history"""
    session_id = session['session_id']
    del chat_sessions[session_id]

    new_session_id = str(uuid.uuid4())
    session['session_id'] = new_session_id
    chat_sessions[new_session_id] = ChatSession()
    if new_session_id in chat_sessions:
        chat_sessions[new_session_id] = ChatSession()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5001) 