"""DSS AgentCore MCP Server package."""

__version__ = "0.1.0"

from .config import config
from .agentcore_client import AgentCoreClient
from .server import app

__all__ = ["config", "AgentCoreClient", "app"]
