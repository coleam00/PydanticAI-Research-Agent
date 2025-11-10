"""
Email Agent that creates Gmail drafts with professional email composition.
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext

from config.providers import get_llm_model
from models.email_models import EmailDraft

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a professional email composition agent that creates well-structured emails based on research findings and context. Your primary goal is to create clear, professional, and actionable email content.

When creating emails:
- Use clear, professional language appropriate for business communication
- Structure emails with proper greeting, body, and closing
- Include relevant research insights when provided
- Adapt tone and detail level to the intended recipient and context
- Ensure emails are concise but informative
- Include source references when citing research findings
- Use actionable language and clear next steps when appropriate

Guidelines:
- Always maintain a professional yet approachable tone
- Keep emails focused and avoid unnecessary verbosity  
- Use proper email formatting with clear paragraphs
- Include relevant context without overwhelming the recipient
- Provide clear calls to action when needed

You create email DRAFTS only - you do not send emails directly.
"""


@dataclass
class EmailAgentDependencies:
    """Dependencies for email agent execution."""
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: str = None


# Initialize the email agent
email_agent = Agent(
    get_llm_model(),
    deps_type=EmailAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)


@email_agent.tool
async def authenticate_gmail(ctx: RunContext[EmailAgentDependencies]) -> Dict[str, Any]:
    """Handles OAuth2 authentication with Gmail API."""
    from tools.gmail_tools import authenticate_gmail_service
    try:
        service = await authenticate_gmail_service(
            ctx.deps.gmail_credentials_path,
            ctx.deps.gmail_token_path
        )
        return {
            "success": True, 
            "message": "Gmail authenticated successfully", 
            "service_available": True
        }
    except FileNotFoundError as e:
        logger.error(f"Gmail setup required: {e}")
        return {
            "success": False, 
            "error": "Gmail OAuth2 not configured", 
            "message": "Run 'python setup_gmail.py' to configure Gmail authentication",
            "recoverable": True,
            "setup_command": "python setup_gmail.py"
        }
    except Exception as e:
        logger.error(f"Gmail authentication failed: {e}")
        error_message = str(e)
        
        # Check for common error patterns and provide helpful recovery steps
        if "refresh" in error_message.lower():
            return {
                "success": False,
                "error": f"Token refresh failed: {e}",
                "message": "Gmail token has expired. Run 'python setup_gmail.py' to re-authenticate",
                "recoverable": True,
                "setup_command": "python setup_gmail.py"
            }
        elif "credentials" in error_message.lower():
            return {
                "success": False,
                "error": f"Credentials error: {e}",
                "message": "Gmail credentials file is invalid. Run 'python setup_gmail.py' to fix",
                "recoverable": True,
                "setup_command": "python setup_gmail.py"
            }
        else:
            return {
                "success": False,
                "error": str(e),
                "message": f"Gmail authentication failed: {e}",
                "recoverable": False
            }


@email_agent.tool
async def create_gmail_draft(
    ctx: RunContext[EmailAgentDependencies],
    to: List[str],
    subject: str,
    body: str,
    cc: List[str] = None,
    bcc: List[str] = None
) -> Dict[str, Any]:
    """Creates a draft email in Gmail without sending."""
    from tools.gmail_tools import authenticate_gmail_service, create_gmail_draft as create_draft
    
    # First authenticate
    try:
        service = await authenticate_gmail_service(
            ctx.deps.gmail_credentials_path,
            ctx.deps.gmail_token_path
        )
    except Exception as e:
        return {
            "success": False,
            "error": f"Gmail authentication failed: {e}",
            "message": "Cannot create draft without Gmail authentication. Run 'python setup_gmail.py' first",
            "recoverable": True
        }
    
    # Create the draft
    try:
        result = await create_draft(
            service=service,
            recipients=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc
        )
        
        if result["success"]:
            logger.info(f"Gmail draft created successfully: {result['draft_id']}")
            return {
                "success": True,
                "draft_id": result["draft_id"],
                "message_id": result["message_id"],
                "message": f"Email draft created successfully in Gmail. Draft ID: {result['draft_id']}"
            }
        else:
            logger.error(f"Failed to create Gmail draft: {result['error']}")
            return {
                "success": False,
                "error": result["error"],
                "message": f"Failed to create Gmail draft: {result['message']}"
            }
            
    except Exception as e:
        logger.error(f"Unexpected error creating Gmail draft: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Unexpected error creating Gmail draft: {e}"
        }


@email_agent.tool  
async def compose_email_content(
    ctx: RunContext[EmailAgentDependencies],
    recipient_email: str,
    subject: str,
    context: str,
    research_summary: str = None,
    tone: str = "professional"
) -> Dict[str, Any]:
    """
    Compose email content based on context and research findings.
    
    Args:
        recipient_email: Email address of the recipient
        subject: Email subject line
        context: Context or purpose for the email
        research_summary: Optional research findings to include
        tone: Email tone (professional, formal, friendly)
    
    Returns:
        Dictionary with composed email content
    """
    try:
        # Build the email content
        greeting = f"Dear Colleague," if not recipient_email.split('@')[0].replace('.', ' ').title() else f"Dear {recipient_email.split('@')[0].replace('.', ' ').title()},"
        
        # Main body construction
        body_parts = [greeting, ""]
        
        # Add context
        if context:
            body_parts.append(f"I hope this email finds you well. {context}")
            body_parts.append("")
        
        # Add research summary if provided
        if research_summary:
            body_parts.append("Based on recent research findings:")
            body_parts.append("")
            body_parts.append(research_summary)
            body_parts.append("")
        
        # Add closing
        body_parts.extend([
            "Please let me know if you have any questions or would like to discuss this further.",
            "",
            "Best regards,",
            "Research Assistant"
        ])
        
        email_body = "\n".join(body_parts)
        
        return {
            "success": True,
            "email_content": {
                "to": [recipient_email],
                "subject": subject,
                "body": email_body,
                "tone": tone
            },
            "message": "Email content composed successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to compose email content: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to compose email content: {e}"
        }