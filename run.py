"""
Entry point to run the Flask application
"""
from app import app

if __name__ == '__main__':
    print("🌐 Starting Chatbot API...")
    print("📍 Open: http://localhost:5000")
    print("🔧 Debug mode activated")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
