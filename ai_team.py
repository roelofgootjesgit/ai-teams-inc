import os
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AITeam:
    def __init__(self):
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def run(self, question: str) -> str:
        """
        Main entry point for AI team collaboration
        Currently uses Claude (can be extended to multi-agent later)
        """
        try:
            # Use Claude for initial response
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            # Extract text from response
            answer = response.content[0].text
            
            return answer
            
        except Exception as e:
            return f"Error: {str(e)}"