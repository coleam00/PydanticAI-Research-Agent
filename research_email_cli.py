"""
Beautiful streaming CLI for Research & Email Agent using Rich library.
"""

import asyncio
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.markdown import Markdown

from pydantic_ai import Agent
from pydantic_ai.messages import PartStartEvent, PartDeltaEvent, TextPart, TextPartDelta
from agents import research_agent, ResearchAgentDependencies
from config.settings import settings

console = Console()


async def stream_agent_response(user_input: str, deps: ResearchAgentDependencies, conversation_history: list):
    """Stream agent response with real-time tool call visibility."""
    
    try:
        # Build context with conversation history
        context = "\n".join(conversation_history[-6:]) if conversation_history else ""
        
        prompt = f"""Previous conversation:
{context}

User: {user_input}

Respond naturally and helpfully."""
        
        # Stream the agent execution
        response_text = ""
        async with research_agent.iter(prompt, deps=deps) as run:

            async for node in run:

                # Handle user prompt node
                if Agent.is_user_prompt_node(node):
                    pass  # Clean start - no processing messages

                # Handle model request node - stream the thinking process
                elif Agent.is_model_request_node(node):
                    # Show assistant prefix at the start
                    console.print("[bold blue]Assistant:[/bold blue] ", end="")

                    # Stream model request events for real-time text
                    async with node.stream(run.ctx) as request_stream:
                        async for event in request_stream:
                            # Handle PartStartEvent - contains the FIRST TOKEN
                            if isinstance(event, PartStartEvent):
                                # Check if this is a text part
                                if isinstance(event.part, TextPart):
                                    # Get the initial content (first token)
                                    initial_content = event.part.content
                                    if initial_content:
                                        console.print(initial_content, end="")
                                        response_text += initial_content

                            # Handle PartDeltaEvent - contains subsequent tokens
                            elif isinstance(event, PartDeltaEvent):
                                # Check if this is a text delta
                                if isinstance(event.delta, TextPartDelta):
                                    delta_text = event.delta.content_delta
                                    if delta_text:
                                        console.print(delta_text, end="")
                                        response_text += delta_text
                
                # Handle tool calls - this is the key part
                elif Agent.is_call_tools_node(node):
                    # Stream tool execution events
                    async with node.stream(run.ctx) as tool_stream:
                        async for event in tool_stream:
                            event_type = type(event).__name__
                            
                            if event_type == "FunctionToolCallEvent":
                                # Extract tool name from the part attribute  
                                tool_name = "Unknown Tool"
                                args = None
                                
                                # Check if the part attribute contains the tool call
                                if hasattr(event, 'part'):
                                    part = event.part
                                    
                                    # Check if part has tool_name directly
                                    if hasattr(part, 'tool_name'):
                                        tool_name = part.tool_name
                                    elif hasattr(part, 'function_name'):
                                        tool_name = part.function_name
                                    elif hasattr(part, 'name'):
                                        tool_name = part.name
                                    
                                    # Check for arguments in part
                                    if hasattr(part, 'args'):
                                        args = part.args
                                    elif hasattr(part, 'arguments'):
                                        args = part.arguments
                                
                                console.print(f"  🔹 [cyan]Calling tool:[/cyan] [bold]{tool_name}[/bold]")
                                
                                # Show tool args if available
                                if args and isinstance(args, dict):
                                    # Show first few characters of each arg
                                    arg_preview = []
                                    for key, value in list(args.items())[:3]:
                                        val_str = str(value)
                                        if len(val_str) > 50:
                                            val_str = val_str[:47] + "..."
                                        arg_preview.append(f"{key}={val_str}")
                                    console.print(f"    [dim]Args: {', '.join(arg_preview)}[/dim]")
                            
                            elif event_type == "FunctionToolResultEvent":
                                # Display tool result
                                result = str(event.tool_return) if hasattr(event, 'tool_return') else "No result"
                                if len(result) > 100:
                                    result = result[:97] + "..."
                                console.print(f"  ✅ [green]Tool call complete.[/green]")
                
                # Handle end node
                elif Agent.is_end_node(node):
                    # Print newline at the very end of streaming
                    console.print()

        # Get final result
        final_result = run.result
        final_output = final_result.output if hasattr(final_result, 'output') else str(final_result)
        
        # Return both streamed text and final output for history
        return (response_text.strip(), final_output)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return ("", f"Error: {e}")


def display_welcome():
    """Display welcome banner."""
    welcome = """
# 🔬 Research & Email Agent CLI

Welcome to the AI-powered research and email assistant!

## Available Commands:
- Type your research queries naturally
- Ask to create email drafts based on research
- Use 'help' for more information
- Use 'exit' or 'quit' to leave

## Examples:
- "Research AI safety trends and email summary to john@company.com"
- "Find latest developments in quantum computing"
- "Create email draft about market analysis for jane.doe@firm.com"

---
    """
    console.print(Panel(Markdown(welcome), title="Welcome", border_style="green"))


def validate_setup():
    """Validate that required setup is complete."""
    try:
        # Check if we can access settings
        if not settings.llm_api_key or settings.llm_api_key == "test_key":
            console.print("[yellow]⚠️  Warning: LLM API key not set. Set LLM_API_KEY in .env file[/yellow]")
        
        if not settings.brave_api_key or settings.brave_api_key == "test_key":
            console.print("[yellow]⚠️  Warning: Brave API key not set. Set BRAVE_API_KEY in .env file[/yellow]")
        
        # Check Gmail setup
        import os
        if not os.path.exists(settings.gmail_credentials_path):
            console.print("[yellow]⚠️  Gmail credentials not found. Run 'python setup_gmail.py' first[/yellow]")
        
        if not os.path.exists(settings.gmail_token_path):
            console.print("[yellow]⚠️  Gmail token not found. Run 'python setup_gmail.py' first[/yellow]")
            
    except Exception as e:
        console.print(f"[red]❌ Configuration error: {e}[/red]")
        return False
    
    return True


async def main():
    """Main conversation loop."""
    
    # Show welcome
    welcome = Panel(
        "[bold blue]🔬 PydanticAI Research & Email Agent[/bold blue]\n\n"
        "[green]Real-time tool execution with Gmail integration[/green]\n"
        "[dim]Type 'exit' to quit, 'help' for commands[/dim]",
        style="blue",
        padding=(1, 2)
    )
    console.print(welcome)
    console.print()
    
    # Validate setup
    if not validate_setup():
        console.print("[yellow]⚠️ Some configuration may be missing. Proceeding with defaults...[/yellow]")
    
    try:
        deps = ResearchAgentDependencies(
            brave_api_key=settings.brave_api_key,
            gmail_credentials_path=settings.gmail_credentials_path,
            gmail_token_path=settings.gmail_token_path
        )
    except Exception as e:
        console.print(f"[red]❌ Failed to create agent dependencies: {e}[/red]")
        sys.exit(1)
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold green]You").strip()
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
                
            if not user_input:
                continue
            
            # Handle help
            if user_input.lower() == 'help':
                help_text = Panel(
                    "[bold]Available Commands:[/bold]\n\n"
                    "• Research queries: 'Research AI trends', 'Find info about X'\n"
                    "• Email creation: 'Create email to user@domain.com about Y'\n"
                    "• Combined: 'Research X and email summary to user@domain.com'\n\n"
                    "[dim]Type 'exit' to quit[/dim]",
                    title="Help",
                    style="blue"
                )
                console.print(help_text)
                console.print()
                continue
            
            # Add to history
            conversation_history.append(f"User: {user_input}")
            
            # Stream the interaction and get response
            streamed_text, final_response = await stream_agent_response(user_input, deps, conversation_history)
            
            # Handle the response display and history
            if streamed_text:
                # Response was streamed, just add spacing and save to history
                console.print()
                conversation_history.append(f"Assistant: {streamed_text}")
            elif final_response and final_response.strip():
                # Response wasn't streamed, display it and save to history
                console.print(f"[bold blue]Assistant:[/bold blue] {final_response}")
                console.print()
                conversation_history.append(f"Assistant: {final_response}")
            else:
                # No response
                console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            continue
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Fatal error: {e}[/red]")
        sys.exit(1)