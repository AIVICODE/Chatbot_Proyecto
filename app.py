"""
Flask API for the chatbot
"""
import sys
import os
from flask import Flask, request, render_template

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.controllers.chatbot_controller import ChatbotController

app = Flask(__name__)
chatbot_controller = ChatbotController()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form.get('mensaje', '').strip()
        if not chatbot_controller.validate_message(message):
            raise ValueError("Invalid message")
        else:
            result = chatbot_controller.process_message(message)
            return render_template('index.html', resultado=result)

    except Exception as e:
        return render_template('index.html', error="Invalid message")


if __name__ == '__main__':
    print("🌐 Starting Chatbot API...")
    print("📍 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
