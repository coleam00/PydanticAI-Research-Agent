"""
Gmail OAuth2 tools and draft creation functionality.
"""

import os
import pickle
import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class MockGmailService:
    """Mock Gmail service for testing purposes."""
    
    def __init__(self):
        self.drafts_created = []
    
    def users(self):
        return MockUsersResource(self.drafts_created)


class MockUsersResource:
    def __init__(self, drafts_created):
        self.drafts_created = drafts_created
    
    def drafts(self):
        return MockDraftsResource(self.drafts_created)


class MockDraftsResource:
    def __init__(self, drafts_created):
        self.drafts_created = drafts_created
    
    def create(self, userId: str, body: Dict[str, Any]):
        """Mock draft creation."""
        draft_id = f"mock_draft_{len(self.drafts_created) + 1}"
        self.drafts_created.append({
            'id': draft_id,
            'userId': userId,
            'body': body
        })
        return MockExecuteResponse({'id': draft_id, 'message': {'id': f"msg_{draft_id}"}})


class MockExecuteResponse:
    def __init__(self, response_data):
        self.response_data = response_data
    
    def execute(self):
        return self.response_data


async def authenticate_gmail_service(credentials_path: str, token_path: str, test_mode: bool = False):
    """Authenticate and return Gmail service instance."""
    # Return mock service for testing
    if test_mode or os.getenv('TESTING') == 'true':
        logger.info("Using mock Gmail service for testing")
        return MockGmailService()
    
    creds = None
    
    # Check if credentials file exists
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Gmail credentials file not found at {credentials_path}. "
            "Run 'python setup_gmail.py' to set up OAuth2 authentication."
        )
    
    # Token loading and refresh logic
    if os.path.exists(token_path):
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            logger.warning(f"Failed to load existing token: {e}")
            # Remove corrupted token file
            if os.path.exists(token_path):
                os.remove(token_path)
    
    # OAuth2 flow if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Successfully refreshed Gmail token")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                raise Exception(
                    f"Failed to refresh Gmail token: {e}. "
                    "Run 'python setup_gmail.py' to re-authenticate."
                )
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("Successfully completed OAuth2 flow")
            except Exception as e:
                logger.error(f"OAuth2 flow failed: {e}")
                raise Exception(
                    f"Gmail OAuth2 authentication failed: {e}. "
                    "Ensure you have downloaded credentials.json from Google Cloud Console."
                )
        
        # Save tokens
        try:
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            logger.info(f"Successfully saved Gmail token to {token_path}")
        except Exception as e:
            logger.warning(f"Failed to save token: {e}")
    
    return build('gmail', 'v1', credentials=creds)


async def create_gmail_draft(
    service, 
    recipients: List[str], 
    subject: str, 
    body: str, 
    cc: List[str] = None, 
    bcc: List[str] = None
) -> Dict[str, Any]:
    """Create a Gmail draft email."""
    try:
        # Create message
        message = MIMEMultipart()
        message['to'] = ', '.join(recipients)
        message['subject'] = subject
        
        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Create draft
        draft_body = {
            'message': {
                'raw': raw_message
            }
        }
        
        result = service.users().drafts().create(
            userId='me',
            body=draft_body
        ).execute()
        
        return {
            'success': True,
            'draft_id': result['id'],
            'message_id': result['message']['id'],
            'message': f"Draft created successfully with ID: {result['id']}"
        }
        
    except Exception as e:
        logger.error(f"Failed to create Gmail draft: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': f"Failed to create Gmail draft: {e}"
        }


def validate_gmail_setup(credentials_path: str, token_path: str) -> Dict[str, Any]:
    """Validate Gmail OAuth2 setup."""
    result = {
        "credentials_exists": os.path.exists(credentials_path),
        "token_exists": os.path.exists(token_path),
        "setup_required": False,
        "messages": []
    }
    
    if not result["credentials_exists"]:
        result["messages"].append(f"Credentials file missing: {credentials_path}")
        result["setup_required"] = True
    
    if not result["token_exists"]:
        result["messages"].append(f"Token file missing: {token_path}")
        result["setup_required"] = True
    
    if result["setup_required"]:
        result["messages"].append("Run 'python setup_gmail.py' to complete OAuth2 setup")
    else:
        result["messages"].append("Gmail OAuth2 appears to be configured")
    
    return result