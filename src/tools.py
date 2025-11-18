"""
Tools that the research agent can use to gather information.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import json


class Tool:
    """Base class for all tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, **kwargs) -> str:
        """Execute the tool and return results as a string."""
        raise NotImplementedError

    def to_function_schema(self) -> Dict[str, Any]:
        """Convert tool to OpenAI function calling schema."""
        raise NotImplementedError


class WebSearchTool(Tool):
    """Simple web search tool using DuckDuckGo's HTML search."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information. Returns titles, snippets, and URLs of search results."
        )

    def execute(self, query: str) -> str:
        """
        Execute a web search and return formatted results.

        Args:
            query: The search query string

        Returns:
            Formatted string with search results
        """
        try:
            # Using DuckDuckGo's HTML interface (no API key needed)
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.post(url, data=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            # Parse search results
            for result in soup.find_all('div', class_='result', limit=5):
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')

                if title_elem:
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })

            if not results:
                return f"No results found for query: {query}"

            # Format results as readable text
            formatted = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                formatted += f"{i}. {result['title']}\n"
                formatted += f"   {result['snippet']}\n"
                formatted += f"   URL: {result['url']}\n\n"

            return formatted.strip()

        except Exception as e:
            return f"Error performing search: {str(e)}"

    def to_function_schema(self) -> Dict[str, Any]:
        """Return OpenAI function calling schema for this tool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to look up"
                        }
                    },
                    "required": ["query"]
                }
            }
        }


class ToolRegistry:
    """Registry to manage available tools."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """Get a tool by name."""
        return self.tools.get(name)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Get all tool schemas for OpenAI function calling."""
        return [tool.to_function_schema() for tool in self.tools.values()]

    def execute(self, name: str, **kwargs) -> str:
        """Execute a tool by name with given arguments."""
        tool = self.get(name)
        if not tool:
            return f"Error: Tool '{name}' not found"
        return tool.execute(**kwargs)


# Create default registry with available tools
def create_default_registry() -> ToolRegistry:
    """Create a registry with default tools."""
    registry = ToolRegistry()
    registry.register(WebSearchTool())
    return registry
