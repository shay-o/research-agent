"""
Main entry point for the research agent CLI.
"""
import os
import sys
from dotenv import load_dotenv
from .agent import ResearchAgent


def main():
    """Run the research agent CLI."""
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        print("See .env.example for the format.")
        sys.exit(1)

    model = os.getenv("MODEL_NAME", "gpt-4o-mini")
    max_iterations = int(os.getenv("MAX_ITERATIONS", "5"))

    print("🤖 Research Agent")
    print("=" * 60)
    print("Ask me anything and I'll research it for you!")
    print("Type 'quit' or 'exit' to stop.\n")

    # Initialize agent
    agent = ResearchAgent(
        api_key=api_key,
        model=model,
        max_iterations=max_iterations,
        verbose=True
    )

    # Interactive loop
    while True:
        try:
            query = input("\n💭 Your question: ").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            # Run the agent
            answer = agent.run(query)

            print(f"\n{'='*60}")
            print("📝 Answer:")
            print(f"{'='*60}")
            print(answer)
            print(f"{'='*60}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    main()
