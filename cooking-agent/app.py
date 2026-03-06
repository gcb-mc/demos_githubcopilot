"""
Cooking AI Agent - Interactive console application powered by GitHub Models.

Usage:
    python app.py          # Start HTTP server mode (default, for production & debugging)
    python app.py --cli    # Start interactive console mode
    python app.py --server # Explicitly start HTTP server mode
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

from tools import search_recipes, extract_ingredients, get_substitutions, convert_units

# Load environment variables (override=True for deployed environments)
load_dotenv(override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
MODEL_ID = os.getenv("MODEL_ID", "openai/gpt-4.1")

SYSTEM_INSTRUCTIONS = """You are Chef AI, a friendly and knowledgeable cooking assistant.

Your capabilities:
1. **Recipe Search**: Find recipes by dish name, cuisine, ingredient, or dietary tags.
2. **Ingredient Extraction**: Break down recipe ingredients into structured lists with quantities, units, and items.
3. **Substitutions**: Suggest ingredient replacements for dietary needs, allergies, or availability.
4. **Unit Conversion**: Convert between common cooking measurements (cups, grams, ounces, etc.).

Guidelines:
- Always be enthusiastic and encouraging about cooking.
- When sharing recipes, present them in a clear, step-by-step format.
- Proactively suggest substitutions when you detect common allergens.
- If the user asks for something outside your tools, use your general knowledge to help.
- Format responses with clear sections using markdown-style headers and bullet points.
- When multiple recipes match, briefly summarize each and let the user choose.
- Always mention prep time and servings when sharing a recipe.

Start by greeting the user and letting them know what you can help with!
"""


def create_agent() -> ChatAgent:
    """Create and configure the cooking AI agent."""
    openai_client = AsyncOpenAI(
        base_url="https://models.github.ai/inference",
        api_key=GITHUB_TOKEN,
    )
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id=MODEL_ID,
    )
    agent = ChatAgent(
        chat_client=chat_client,
        name="ChefAI",
        instructions=SYSTEM_INSTRUCTIONS,
        tools=[search_recipes, extract_ingredients, get_substitutions, convert_units],
    )
    return agent


async def run_cli() -> None:
    """Run the agent in interactive console mode."""
    agent = create_agent()
    thread = agent.get_new_thread()

    print("=" * 60)
    print("  🍳 Chef AI - Your Cooking Assistant")
    print("=" * 60)
    print("  Type your question about cooking, recipes, or ingredients.")
    print("  Type 'quit' or 'exit' to leave.\n")

    # Initial greeting
    print("Chef AI: ", end="", flush=True)
    async for chunk in agent.run_stream("Hello! I'd like help with cooking.", thread=thread):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")

    # Conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! Happy cooking! 🍽️")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nGoodbye! Happy cooking! 🍽️")
            break

        print("\nChef AI: ", end="", flush=True)
        async for chunk in agent.run_stream(user_input, thread=thread):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")


async def run_server() -> None:
    """Run the agent as an HTTP server for production and debugging."""
    try:
        from azure.ai.agentserver.agentframework import from_agent_framework
    except ImportError:
        print("ERROR: Server mode requires azure-ai-agentserver-agentframework.")
        print("Install with: pip install azure-ai-agentserver-core==1.0.0b10 azure-ai-agentserver-agentframework==1.0.0b10")
        print("\nFalling back to CLI mode...\n")
        await run_cli()
        return

    agent = create_agent()
    await from_agent_framework(agent).run_async()


def main() -> None:
    """Entry point: parse args and launch the appropriate mode."""
    if "--cli" in sys.argv:
        asyncio.run(run_cli())
    else:
        # Default to HTTP server mode (--server or no flag)
        asyncio.run(run_server())


if __name__ == "__main__":
    main()
