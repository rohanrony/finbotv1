import openai
import os
from typing import List, Dict, Optional

class LLMClient:
    """Wrapper for OpenAI API to handle chat interactions."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_answer(self, prompt: str, history: List[Dict] = None) -> str:
        """
        Generate an answer using OpenAI.
        """
        if not self.api_key or not self.client:
            return "Please provide an OpenAI API key in the Settings tab to enable chat."
            
        try:
            messages = [{"role": "system", "content": "You are a professional financial analyst."}]
            # Add history if needed, but current engine sends full prompt with history
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response from OpenAI: {str(e)}"
