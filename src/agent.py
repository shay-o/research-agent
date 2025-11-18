"""
Core agent implementation with reasoning loop.
"""
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .tools import ToolRegistry, create_default_registry


class ResearchAgent:
    """
    A research agent that can reason about tasks and use tools to gather information.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        max_iterations: int = 5,
        verbose: bool = True
    ):
        """
        Initialize the research agent.

        Args:
            api_key: OpenAI API key
            model: Model to use for reasoning
            max_iterations: Maximum number of reasoning iterations
            verbose: Whether to print detailed logs
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.tool_registry = create_default_registry()

        # System prompt that defines the agent's behavior
        self.system_prompt = """You are a research assistant that helps users find and synthesize information.

You have access to tools that you can use to gather information. When given a question or research task:
1. Break down what information you need to find
2. Use the web_search tool to gather relevant information
3. Analyze and synthesize the results
4. Provide a clear, well-sourced answer

Always cite your sources by mentioning which search results you used.
If you need more information, perform additional searches.
When you have enough information to answer the question, provide your final answer."""

    def run(self, user_query: str) -> str:
        """
        Run the agent on a user query.

        Args:
            user_query: The research question or task

        Returns:
            The agent's final answer
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🔍 Research Query: {user_query}")
            print(f"{'='*60}\n")

        # Initialize conversation with system prompt and user query
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_query}
        ]

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1

            if self.verbose:
                print(f"\n--- Iteration {iteration} ---")

            # Get agent's next action
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tool_registry.get_schemas(),
                tool_choice="auto"
            )

            message = response.choices[0].message
            messages.append(message)

            # Check if agent wants to use tools
            if message.tool_calls:
                if self.verbose:
                    print(f"🛠️  Agent is using {len(message.tool_calls)} tool(s)...")

                # Execute each tool call
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if self.verbose:
                        print(f"   → {function_name}({function_args})")

                    # Execute the tool
                    result = self.tool_registry.execute(function_name, **function_args)

                    if self.verbose:
                        print(f"   ✓ Got {len(result)} characters of results")

                    # Add tool result to conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": result
                    })

            # Check if agent has finished (no tool calls and has content)
            elif message.content:
                if self.verbose:
                    print(f"✅ Agent has formulated final answer")
                return message.content

            else:
                # Safety check: shouldn't reach here
                if self.verbose:
                    print("⚠️  Agent returned no content and no tool calls")
                break

        # Max iterations reached
        if self.verbose:
            print(f"\n⚠️  Reached maximum iterations ({self.max_iterations})")

        # Try to get a final response
        messages.append({
            "role": "user",
            "content": "Please provide your best answer based on the information gathered so far."
        })

        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return final_response.choices[0].message.content


class AgentMemory:
    """
    Optional: Simple memory system to track what the agent has learned.
    This can be extended for more sophisticated agents.
    """

    def __init__(self):
        self.searches_performed: List[str] = []
        self.findings: List[Dict[str, Any]] = []

    def add_search(self, query: str):
        """Record a search query."""
        self.searches_performed.append(query)

    def add_finding(self, source: str, information: str):
        """Record a finding from a source."""
        self.findings.append({
            "source": source,
            "information": information
        })

    def get_summary(self) -> str:
        """Get a summary of what has been learned."""
        summary = f"Performed {len(self.searches_performed)} searches:\n"
        for i, query in enumerate(self.searches_performed, 1):
            summary += f"{i}. {query}\n"
        summary += f"\nGathered {len(self.findings)} findings."
        return summary

    # TODO(human): Implement synthesize_findings method
    def synthesize_findings(self) -> str:
        """
        Synthesize all findings into a coherent summary.

        This method should:
        - Look at all the findings in self.findings
        - Identify common themes or key points
        - Return a well-structured summary

        Returns:
            A synthesized summary of all findings
        """
        pass
