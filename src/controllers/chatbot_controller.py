"""
Chatbot controller
Handles control logic and orchestration
"""
from typing import Dict, Any
from ..services.chatbot_service import ChatbotService


class ChatbotController:
    """Controller that manages chatbot operations"""
    
    def __init__(self):
        """Initialize the controller with the service"""
        self.chatbot_service = ChatbotService()

    def process_message(self, message: str) -> Dict[str, Any]:
        """Process message and return structured result"""
        try:
            prerouting_result = self.chatbot_service.prerouting(message)
            prompt = self.chatbot_service.generate_prompt(prerouting_result, message)
            llm_response = self.chatbot_service.process_message(message)

            return {
                "mensaje_original": message,
                "es_valido": True,
                "respuesta": llm_response,
                "prompt_usado": prompt,
                "analisis": prerouting_result
            }
        except Exception as e:
            return {
                "mensaje_original": message,
                "es_valido": False,
                "respuesta": f"Error processing message: {str(e)}",
                "prompt_usado": "",
                "analisis": {}
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
