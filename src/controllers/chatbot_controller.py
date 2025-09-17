"""
Chatbot controller
Handles control logic and orchestration
"""
from typing import Dict, Any
from services.chatbot_service import ChatbotService


class ChatbotController:
    """Controller that manages chatbot operations"""
    
    def __init__(self):
        """Initialize the controller with the service"""
        self.chatbot_service = ChatbotService()

    def process_message(self, message: str) -> Dict[str, Any]:
        """Process message and return structured result"""
        try:
            prerouting_result = self.chatbot_service.prerouting(message)

            print(f"Prerouting result: {prerouting_result}")
            
            # Generate context based on intent
            context = self.chatbot_service.generate_context(message, prerouting_result)
            
            # Generate prompt with all context
            prompt = self.chatbot_service.generate_prompt(message, prerouting_result, context)
            
            llm_response = self.chatbot_service.process_message(message, prompt)
            
            return {
                "original_message": message,
                "is_valid": True,
                "response": llm_response,
                "prompt_used": prompt,
                "intent": prerouting_result,
                "context": context
            }
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return {
                "original_message": message,
                "is_valid": False,
                "response": f"I'm sorry, I encountered an error while processing your message. Please try again.",
                "prompt_used": "",
                "intent": "error",
                "context": {},
                "error": str(e)
            }

    def validate_message(self, message: str) -> bool:
        """
        Validate input message
        """
        if not message or not message.strip():
            return False
        if len(message.strip()) < 1:
            return False
        return True
