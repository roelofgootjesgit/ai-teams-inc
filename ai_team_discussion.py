"""
GTS AI Teams - Discussion System
Agents engage in multi-round discussions, building on each other's insights
"""

import os
from anthropic import Anthropic
from typing import List, Dict

class AITeam:
    """Multi-agent AI team with discussion capabilities"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Define our 3 agents
        self.agents = {
            "pm": {
                "name": "Project Manager",
                "icon": "🎯",
                "role": "You are a Project Manager who coordinates AI projects and synthesizes team discussions."
            },
            "architect": {
                "name": "AI Architect", 
                "icon": "🏗️",
                "role": "You are an AI Architect specializing in system design and technical implementation."
            },
            "expert": {
                "name": "Domain Expert",
                "icon": "💼",
                "role": "You are a Domain Expert focused on business value and practical constraints."
            }
        }
    
    def run(self, question: str) -> str:
        """Process question through multi-round discussion system"""
        
        responses = []
        discussion_history = []
        
        # === ROUND 1: OPENING STATEMENTS ===
        
        # PM opens discussion
        pm_opening = self._get_response(
            "pm",
            f"""Question: {question}

As Project Manager, open this discussion by:
1. Breaking down the question into key aspects
2. Identifying what Architect should address (technical/architecture)
3. Identifying what Expert should address (business/practical)

Keep it concise (3-4 sentences)."""
        )
        
        responses.append(self._create_response("pm", pm_opening, "OPENING"))
        discussion_history.append(f"PM: {pm_opening}")
        
        # Architect responds
        architect_initial = self._get_response(
            "architect",
            f"""Question: {question}

{self._format_history(discussion_history)}

Provide your technical perspective. Be specific about architecture, technologies, and implementation approach. (3-4 sentences)"""
        )
        
        responses.append(self._create_response("architect", architect_initial, "INITIAL"))
        discussion_history.append(f"Architect: {architect_initial}")
        
        # Expert responds
        expert_initial = self._get_response(
            "expert",
            f"""Question: {question}

{self._format_history(discussion_history)}

Provide your business/practical perspective. Focus on real-world constraints, ROI, and implementation challenges. (3-4 sentences)"""
        )
        
        responses.append(self._create_response("expert", expert_initial, "INITIAL"))
        discussion_history.append(f"Expert: {expert_initial}")
        
        # === ROUND 2: DISCUSSION & DEBATE ===
        
        # Architect responds to Expert's concerns
        architect_response = self._get_response(
            "architect",
            f"""Question: {question}

{self._format_history(discussion_history)}

The Domain Expert raised important practical concerns. Address these concerns from a technical standpoint. If you agree, explain how to implement it. If you disagree, provide technical reasoning. Reference the Expert's points. (3-4 sentences)

Start with "@Expert:" to show you're responding."""
        )
        
        responses.append(self._create_response("architect", architect_response, "RESPONSE"))
        discussion_history.append(f"Architect: {architect_response}")
        
        # Expert responds to Architect's technical approach
        expert_response = self._get_response(
            "expert",
            f"""Question: {question}

{self._format_history(discussion_history)}

The Architect proposed a technical approach. Evaluate it from a business/practical perspective. Does it address real-world constraints? Is there a simpler path? Reference the Architect's points. (3-4 sentences)

Start with "@Architect:" to show you're responding."""
        )
        
        responses.append(self._create_response("expert", expert_response, "RESPONSE"))
        discussion_history.append(f"Expert: {expert_response}")
        
        # === ROUND 3: SYNTHESIS ===
        
        # PM synthesizes the discussion
        pm_synthesis = self._get_response(
            "pm",
            f"""Question: {question}

{self._format_history(discussion_history)}

As Project Manager, synthesize this discussion into:
1. Key consensus points between Architect and Expert
2. Any remaining trade-offs or decisions needed
3. Recommended action plan combining both perspectives

Be decisive and actionable. (4-5 sentences)"""
        )
        
        responses.append(self._create_response("pm", pm_synthesis, "SYNTHESIS"))
        
        # Format the response
        return self._format_response(responses)
    
    def _get_response(self, agent_key: str, prompt: str) -> str:
        """Get response from a specific agent"""
        
        agent = self.agents[agent_key]
        
        system_prompt = f"""{agent['role']}

You are part of a multi-agent discussion. Build on previous points and reference other agents when responding.

Keep responses focused and concise (3-5 sentences). Be direct and actionable."""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                temperature=0.8,  # Slightly higher for more diverse discussion
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _create_response(self, agent_key: str, content: str, stage: str) -> Dict[str, str]:
        """Create a formatted response dict"""
        agent = self.agents[agent_key]
        
        # Add stage label to agent name
        stage_labels = {
            "OPENING": "OPENING",
            "INITIAL": "INITIAL",
            "RESPONSE": "RESPONSE",
            "SYNTHESIS": "SYNTHESIS"
        }
        
        display_name = f"{agent['name']}"
        if stage in stage_labels:
            display_name += f" - {stage_labels[stage]}"
        
        return {
            "agent": display_name,
            "icon": agent['icon'],
            "content": content
        }
    
    def _format_history(self, history: List[str]) -> str:
        """Format discussion history for context"""
        if not history:
            return ""
        
        return "Discussion so far:\n" + "\n".join([f"- {h}" for h in history[-3:]])  # Last 3 messages
    
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
    
    print("Testing Multi-Agent Discussion System...")
    print("="*70)
    
    # Test question
    response = team.run("How do I build a recommendation system?")
    
    print(response)
    print("="*70)
    print("\nDiscussion complete!")