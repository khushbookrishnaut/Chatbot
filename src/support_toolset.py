import asyncio
from typing import Any

# ---------------------------------------------------------
# Dummy Knowledge Base (Member 2's rules go here)
# ---------------------------------------------------------
COMPANY_POLICY = {
    "refund": "Refunds take 5-7 business days. Only applicable within 30 days of purchase.",
    "return": "Items can be returned if unused and in original packaging. Electronics have a 15-day return window.",
    "shipping": "Standard shipping takes 3-5 days. Expedited is 1-2 days.",
    "damaged": "If a product is damaged, please upload a photo within 48 hours for a free replacement."
}

class SupportToolset:
    """Intelligent Customer Support Toolset"""

    def __init__(self):
        # Database ki jagah hum escalate hue tickets ko is list mein save karenge
        self.escalated_tickets = []

    async def search_knowledge_base(self, topic: str) -> str:
        """
        Search the company policy for answers.
        Use this tool FIRST when a user asks about rules, refunds, returns, or policies.
        
        Args:
            topic: The main subject (e.g., 'refund', 'return', 'shipping')
            
        Returns:
            str: Policy details or a 'not found' message
        """
        try:
            if not topic.strip():
                return "Error: No topic provided for search."

            topic_lower = topic.lower()
            
            # Policy dictionary mein keyword dhundhna
            for key, policy_text in COMPANY_POLICY.items():
                if key in topic_lower:
                    return f"Knowledge Base Result: {policy_text}"
            
            return "Error: No specific policy found for this topic. If the user insists, you must escalate the issue."
            
        except Exception as e:
            return f"Search failed: {str(e)}"

    async def escalate_to_human(self, summary: str, reason: str) -> str:
        """
        Escalate the conversation to a human support agent.
        Use this ONLY when the policy doesn't cover the issue, the user is angry, or asks to speak to a human.
        
        Args:
            summary: Brief summary of the user's problem
            reason: Why this needs human intervention
            
        Returns:
            str: Success message with Ticket ID
        """
        try:
            # Simulate a small delay for realistic processing
            await asyncio.sleep(0.5) 
            
            # Ek unique ticket ID generate karna
            ticket_id = f"TKT-100{len(self.escalated_tickets) + 1}"
            
            # Ticket ko save karna
            ticket_data = {
                "ticket_id": ticket_id,
                "summary": summary,
                "reason": reason,
                "status": "Escalated to Human"
            }
            self.escalated_tickets.append(ticket_data)
            
            # Print command backend terminal mein dikhega (Judges ke liye log)
            print(f"\n🚨 [SYSTEM ALERT] NEW ESCALATION: {ticket_data}\n")
            
            return f"Success: Issue escalated. Ticket ID is {ticket_id}. Inform the user that a human agent will contact them soon."
            
        except Exception as e:
            return f"Escalation failed: {str(e)}"

    def get_tools(self) -> dict[str, Any]:
        """Return dictionary of available tools for OpenAI function calling"""
        return {
            'search_knowledge_base': self,
            'escalate_to_human': self,
        }