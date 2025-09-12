"""
Flask API for @app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form.get('message', '').strip()
        if not chatbot_controller.validate_message(message):
            raise ValueError("Invalid message")
        else:
            result = chatbot_controller.process_message(message)
            return render_template('index.html', result=result)

    except Exception as e:
        return render_template('index.html', error="Invalid message")
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
        # The form uses 'message' as the input name in the template
        message = request.form.get('message', '').strip()
        if not chatbot_controller.validate_message(message):
            raise ValueError("Invalid message")
        else:
            result = chatbot_controller.process_message(message)
            # Render using 'result' so template can access it consistently
            return render_template('index.html', result=result)

    except Exception as e:
        # Return the exception message for easier debugging in the frontend
        return render_template('index.html', error=str(e))


if __name__ == '__main__':
    print("🌐 Starting Chatbot API...")
    print("📍 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
