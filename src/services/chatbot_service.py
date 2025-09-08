"""
Chatbot service
Contains the main business logic
"""
from typing import Dict, Any

class ChatbotService:
    """Service that encapsulates the chatbot business logic"""
    
    def prerouting(self, message: str) -> Dict[str, Any]:
        """Preliminary analysis of the message"""
        return {
            "length": len(message),
            "word_count": len(message.split()),
            "has_question": "?" in message
        }
    
    def generate_prompt(self, prerouting_result: Dict[str, Any], message: str) -> str:
        """Generate prompt for the LLM"""
        return f"User says: {message}. Analysis: {prerouting_result}"
    
    def process_message(self, message: str) -> str:
        """Process message and generate response"""
        # Simple responses based on content
        message_lower = message.lower()
        
        if "hello" in message_lower or "hi" in message_lower or "hola" in message_lower:
            return "Hello! How can I help you today?"
        elif "how are you" in message_lower or "como estas" in message_lower:
            return "I'm doing great, thank you for asking! How are you?"
        elif "bye" in message_lower or "goodbye" in message_lower or "adios" in message_lower:
            return "Goodbye! Have a great day!"
        elif "?" in message:
            return f"Interesting question about '{message}'. Let me help you think about that."
        else:
            return f"I received your message: '{message}'. Is there something specific I can help you with?"

