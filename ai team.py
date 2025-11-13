"""
GTS AI Teams - Multi-Agent System
Simplified version with guaranteed multi-agent responses
"""

import os
from anthropic import Anthropic
from typing import List, Dict

class AITeam:
    """Multi-agent AI team coordinator"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Define our 3 agents
        self.agents = {
            "pm": {
                "name": "Project Manager",
                "icon": "🎯",
                "role": "You are a Project Manager who coordinates AI projects. Be brief (2-3 sentences). Focus on: task breakdown, team coordination, what other experts should address."
            },
            "architect": {
                "name": "AI Architect", 
                "icon": "🏗️",
                "role": "You are an AI Architect specializing in system design. Be brief (2-3 sentences). Focus on: technical architecture, implementation approaches, scalability."
            },
            "expert": {
                "name": "Domain Expert",
                "icon": "💼",
                "role": "You are a Domain Expert focused on business value. Be brief (2-3 sentences). Focus on: practical considerations, business impact, real-world constraints."
            }
        }
    
    def run(self, question: str) -> str:
        """Process question through multi-agent system"""
        
        responses = []
        
        # Step 1: Project Manager analyzes and coordinates
        pm_response = self._get_agent_response(
            "pm", 
            question,
            "Analyze this question and state which aspects the AI Architect and Domain Expert should address. Keep it very brief."
        )
        responses.append({
            "agent": self.agents["pm"]["name"],
            "icon": self.agents["pm"]["icon"],
            "content": pm_response
        })
        
        # Step 2: AI Architect provides technical perspective
        architect_prompt = f"""Question: {question}

Project Manager's coordination: {pm_response}

Provide your technical/architectural perspective. Be concise (2-3 sentences max)."""
        
        architect_response = self._get_agent_response("architect", architect_prompt, "")
        responses.append({
            "agent": self.agents["architect"]["name"],
            "icon": self.agents["architect"]["icon"],
            "content": architect_response
        })
        
        # Step 3: Domain Expert provides business/practical perspective
        expert_prompt = f"""Question: {question}

Project Manager: {pm_response}
AI Architect: {architect_response}

Provide your business/practical perspective. Be concise (2-3 sentences max)."""
        
        expert_response = self._get_agent_response("expert", expert_prompt, "")
        responses.append({
            "agent": self.agents["expert"]["name"],
            "icon": self.agents["expert"]["icon"],
            "content": expert_response
        })
        
        # Format the response
        return self._format_response(responses)
    
    def _get_agent_response(self, agent_key: str, question: str, instruction: str) -> str:
        """Get response from a specific agent"""
        
        agent = self.agents[agent_key]
        
        system_prompt = f"""{agent['role']}

{instruction if instruction else 'Provide your expert perspective.'}

CRITICAL: Keep your response to 2-3 sentences maximum. Be direct and actionable."""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,  # Force brevity
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            return message.content[0].text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _format_response(self, responses: List[Dict[str, str]]) -> str:
        """Format multi-agent response with exact separator format"""
        
        formatted = []
        
        for i, response in enumerate(responses):
            # Add separator between agents (exactly 60 equals)
            if i > 0:
                formatted.append("=" * 60)
            
            # Agent header: icon + name (uppercase)
            formatted.append(f"{response['icon']} {response['agent'].upper()}")
            
            # Separator line (exactly 60 dashes)
            formatted.append("-" * 60)
            
            # Agent content
            formatted.append(response['content'])
            
            # Empty line
            formatted.append("")
        
        return "\n".join(formatted)


# Factory function
def create_team():
    """Create and return AI team instance"""
    return AITeam()


# Test
if __name__ == "__main__":
    import sys
    
    # Check if ANTHROPIC_API_KEY is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in environment")
        sys.exit(1)
    
    team = create_team()
    
    print("Testing Multi-Agent System...")
    print("="*70)
    
    # Test question
    response = team.run("How do I build a recommendation system?")
    
    print(response)
    print("="*70)
    print("\nTest complete!")