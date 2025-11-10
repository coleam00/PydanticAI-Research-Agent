"""
Gmail OAuth2 Setup Wizard for Research Agent.

This script guides users through Gmail OAuth2 setup for the first time.
"""

import os
import sys
import pickle
import webbrowser
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

console = Console()

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def display_welcome():
    """Display welcome message and setup instructions."""
    welcome_text = """
# Gmail OAuth2 Setup Wizard

This wizard will help you set up Gmail OAuth2 authentication for the Research Agent.

## Prerequisites:
1. **Google Cloud Project** with Gmail API enabled
2. **OAuth2 Credentials** downloaded from Google Cloud Console
3. **Internet connection** for authentication flow

## What this script will do:
- Guide you through credential file setup
- Run OAuth2 authentication flow
- Test Gmail API connection
- Save authentication tokens securely
    """
    
    console.print(Panel(Markdown(welcome_text), title="Gmail Setup", border_style="blue"))


def check_credentials_file(credentials_path: str) -> bool:
    """Check if credentials file exists and is valid."""
    if not os.path.exists(credentials_path):
        return False
    
    try:
        # Try to parse the credentials file
        with open(credentials_path, 'r') as f:
            import json
            data = json.load(f)
            return 'installed' in data or 'web' in data
    except Exception as e:
        console.print(f"[red]Error reading credentials file: {e}[/red]")
        return False


def guide_credentials_download():
    """Guide user through credentials download process."""
    instructions = """
# Download Gmail API Credentials

## Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one

## Step 2: Enable Gmail API
1. Go to **APIs & Services > Library**
2. Search for "Gmail API"
3. Click **Enable**

## Step 3: Create OAuth2 Credentials
1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS**
3. Select **OAuth 2.0 Client IDs**
4. Choose **Desktop application**
5. Give it a name (e.g., "Research Agent")
6. Click **CREATE**

## Step 4: Download Credentials
1. Click the **Download** button (⬇) next to your OAuth client
2. Save the file as `credentials.json` in this directory
3. **Never commit this file to version control!**
    """
    
    console.print(Panel(Markdown(instructions), title="Download Instructions", border_style="yellow"))
    
    # Optionally open browser to Google Cloud Console
    if Confirm.ask("Open Google Cloud Console in browser?", default=True):
        webbrowser.open("https://console.cloud.google.com/apis/credentials")


def run_oauth_flow(credentials_path: str, token_path: str) -> bool:
    """Run OAuth2 authentication flow."""
    try:
        console.print("\n[yellow]Starting OAuth2 authentication flow...[/yellow]")
        
        # Create OAuth2 flow
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES
        )
        
        console.print("[blue]Opening browser for authentication...[/blue]")
        creds = flow.run_local_server(port=0)
        
        # Save token
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        
        console.print(f"[green]✓ Authentication successful! Token saved to {token_path}[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Authentication failed: {e}[/red]")
        return False


def test_gmail_connection(token_path: str) -> bool:
    """Test Gmail API connection."""
    try:
        console.print("\n[yellow]Testing Gmail API connection...[/yellow]")
        
        # Load credentials
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        
        # Build service
        service = build('gmail', 'v1', credentials=creds)
        
        # Test with a simple API call
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress')
        
        console.print(f"[green]✓ Gmail API connection successful![/green]")
        console.print(f"[green]✓ Connected to: {email_address}[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Gmail API connection failed: {e}[/red]")
        return False


def create_env_example():
    """Create .env.example with Gmail configuration."""
    env_content = """# Gmail OAuth2 Configuration
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.pickle

# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4o

# Brave Search Configuration
BRAVE_API_KEY=your-brave-api-key
"""
    
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w') as f:
            f.write(env_content)
        console.print("[green]✓ Created .env.example with Gmail configuration[/green]")


def main():
    """Main setup function."""
    display_welcome()
    
    # Get paths from environment or defaults
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
    token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.pickle')
    
    console.print(f"[blue]Credentials path: {credentials_path}[/blue]")
    console.print(f"[blue]Token path: {token_path}[/blue]\n")
    
    # Check for existing setup
    if os.path.exists(token_path):
        if Confirm.ask("Gmail already appears to be set up. Re-run setup?", default=False):
            os.remove(token_path)
        else:
            # Test existing setup
            if test_gmail_connection(token_path):
                console.print("\n[green]Gmail is already configured and working![/green]")
                return True
            else:
                console.print("[yellow]Existing setup appears broken. Continuing with fresh setup...[/yellow]")
    
    # Check credentials file
    if not check_credentials_file(credentials_path):
        console.print(f"[yellow]Credentials file not found or invalid: {credentials_path}[/yellow]")
        guide_credentials_download()
        
        # Wait for user to download credentials
        while not check_credentials_file(credentials_path):
            if not Confirm.ask(f"Have you saved credentials.json to {credentials_path}?"):
                console.print("[red]Setup cancelled. Please download credentials.json first.[/red]")
                return False
            
            if not check_credentials_file(credentials_path):
                console.print("[red]Credentials file still not found or invalid.[/red]")
    
    console.print("[green]✓ Credentials file found and valid[/green]")
    
    # Run OAuth2 flow
    if not run_oauth_flow(credentials_path, token_path):
        console.print("[red]Setup failed during OAuth2 flow.[/red]")
        return False
    
    # Test connection
    if not test_gmail_connection(token_path):
        console.print("[red]Setup failed during connection test.[/red]")
        return False
    
    # Create environment example
    create_env_example()
    
    # Success message
    success_message = """
# Gmail Setup Complete! ✅

## What was configured:
- OAuth2 credentials validated
- Authentication tokens generated and saved
- Gmail API connection tested successfully

## Next steps:
1. Copy `.env.example` to `.env`
2. Add your other API keys (OpenAI, Brave)
3. Run the research agent: `python research_email_cli.py`

## Security reminders:
- **Never commit credentials.json or token.pickle to version control**
- Add them to your .gitignore file
- Keep your API keys secure in the .env file
    """
    
    console.print(Panel(Markdown(success_message), title="Setup Complete", border_style="green"))
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        sys.exit(1)