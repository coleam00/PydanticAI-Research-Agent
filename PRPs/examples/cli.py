"""
Interactive CLI for the PydanticAI Research Agent.

This script allows users to interact with the research agent directly from the command line.
It can run in both interactive mode and automated mode for testing.
"""

import asyncio
import sys
import os
from typing import Optional
from dotenv import load_dotenv
import argparse
import logging

from agents.research_agent import research_agent
from agents.dependencies import ResearchAgentDependencies

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_dependencies() -> ResearchAgentDependencies:
    """Setup agent dependencies from environment variables."""

    brave_api_key = os.getenv("BRAVE_API_KEY")
    if not brave_api_key:
        logger.error("BRAVE_API_KEY not found in environment variables")
        logger.error("Please set BRAVE_API_KEY in your .env file")
        sys.exit(1)

    gmail_creds = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials/gmail_credentials.json")
    gmail_token = os.getenv("GMAIL_TOKEN_PATH", "credentials/gmail_token.json")

    return ResearchAgentDependencies(
        brave_api_key=brave_api_key,
        gmail_credentials_path=gmail_creds,
        gmail_token_path=gmail_token,
        session_id="cli_session"
    )


async def run_query(query: str, deps: ResearchAgentDependencies, verbose: bool = False) -> dict:
    """
    Run a single query through the research agent.

    Args:
        query: The user's query
        deps: Agent dependencies
        verbose: Whether to print verbose output

    Returns:
        Dictionary with result data
    """
    try:
        if verbose:
            print(f"\n🔍 Processing query: {query}")
            print("=" * 60)

        result = await research_agent.run(query, deps=deps)

        if verbose:
            print(f"\n✅ Agent Response:\n")
            print(result.output)
            print("\n" + "=" * 60)
            print(f"📊 Usage: {result.usage}")
            print("=" * 60)

        return {
            "success": True,
            "output": result.output,
            "usage": result.usage,
            "error": None
        }

    except Exception as e:
        logger.error(f"Error running query: {e}", exc_info=True)

        if verbose:
            print(f"\n❌ Error: {str(e)}\n")

        return {
            "success": False,
            "output": None,
            "usage": None,
            "error": str(e)
        }


async def interactive_mode(deps: ResearchAgentDependencies):
    """Run the agent in interactive mode."""

    print("\n" + "=" * 60)
    print("🤖 PydanticAI Research Agent - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type your research query and press Enter")
    print("  - Type 'quit' or 'exit' to exit")
    print("  - Type 'help' for available commands")
    print("=" * 60 + "\n")

    while True:
        try:
            query = input("\n💬 Your query: ").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break

            if query.lower() == 'help':
                print("\n📚 Available Commands:")
                print("  - search [topic]: Search for information")
                print("  - quit/exit: Exit the application")
                print()
                continue

            # Run the query
            await run_query(query, deps, verbose=True)

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!\n")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"\n❌ Unexpected error: {e}\n")


async def automated_mode(query: str, deps: ResearchAgentDependencies, quiet: bool = False):
    """
    Run the agent in automated mode with a single query.

    Args:
        query: The query to run
        deps: Agent dependencies
        quiet: If True, only output JSON result
    """
    result = await run_query(query, deps, verbose=not quiet)

    if quiet:
        import json
        print(json.dumps({
            "success": result["success"],
            "has_output": result["output"] is not None,
            "error": result["error"]
        }))

    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


def main():
    """Main entry point for the CLI."""

    parser = argparse.ArgumentParser(
        description="PydanticAI Research Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python cli.py

  Automated mode:
    python cli.py --query "Search for PydanticAI tutorials"

  Quiet mode (for testing):
    python cli.py --query "What is Python?" --quiet
        """
    )

    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Run a single query in automated mode"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output (useful for testing)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)

    # Setup dependencies
    try:
        deps = setup_dependencies()
    except Exception as e:
        logger.error(f"Failed to setup dependencies: {e}")
        sys.exit(1)

    # Run in appropriate mode
    if args.query:
        asyncio.run(automated_mode(args.query, deps, args.quiet))
    else:
        asyncio.run(interactive_mode(deps))


if __name__ == "__main__":
    main()
