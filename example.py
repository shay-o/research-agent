#!/usr/bin/env python3
"""
Example script showing how to use the Research Agent programmatically.

This demonstrates using the agent as a library rather than through the CLI.
"""
import os
from dotenv import load_dotenv
from src.agent import ResearchAgent


def example_basic_usage():
    """Basic example: Ask a single question."""
    print("="*60)
    print("Example 1: Basic Usage")
    print("="*60)

    # Load API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: Please set OPENAI_API_KEY in .env file")
        return

    # Create agent
    agent = ResearchAgent(
        api_key=api_key,
        model="gpt-4o-mini",
        verbose=True  # Show the thinking process
    )

    # Ask a question
    question = "What is the ReAct pattern in AI agents?"
    answer = agent.run(question)

    print("\n" + "="*60)
    print("FINAL ANSWER:")
    print("="*60)
    print(answer)


def example_multiple_queries():
    """Example: Multiple queries with the same agent."""
    print("\n\n" + "="*60)
    print("Example 2: Multiple Queries")
    print("="*60)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: Please set OPENAI_API_KEY in .env file")
        return

    # Create agent with less verbose output
    agent = ResearchAgent(
        api_key=api_key,
        model="gpt-4o-mini",
        verbose=False  # Hide the thinking process
    )

    # Ask multiple questions
    questions = [
        "What are the benefits of Python for AI development?",
        "How does OpenAI's function calling work?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i} ---")
        print(f"Q: {question}")
        answer = agent.run(question)
        print(f"A: {answer[:200]}...")  # Show first 200 chars


def example_with_custom_settings():
    """Example: Using custom settings."""
    print("\n\n" + "="*60)
    print("Example 3: Custom Settings")
    print("="*60)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: Please set OPENAI_API_KEY in .env file")
        return

    # Create agent with custom settings
    agent = ResearchAgent(
        api_key=api_key,
        model="gpt-4o-mini",
        max_iterations=3,  # Limit to 3 iterations
        verbose=True
    )

    question = "What's the capital of France?"
    print(f"\nQuestion: {question}")
    answer = agent.run(question)

    print("\nThis simple question should complete quickly with fewer iterations!")
    print(f"Answer: {answer}")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║        Research Agent - Example Usage                  ║
    ║                                                        ║
    ║  This script demonstrates different ways to use        ║
    ║  the Research Agent programmatically.                  ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # Run examples
    try:
        example_basic_usage()

        # Uncomment to run more examples:
        # example_multiple_queries()
        # example_with_custom_settings()

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nError running examples: {e}")
        print("Make sure you have:")
        print("1. Created a .env file with your OPENAI_API_KEY")
        print("2. Installed dependencies: pip install -r requirements.txt")
