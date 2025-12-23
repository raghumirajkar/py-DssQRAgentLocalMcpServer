"""MCP Server for AWS AgentCore Supervisor Agent."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .agentcore_client import AgentCoreClient
from .config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Initialize AgentCore client
agentcore_client = AgentCoreClient()

# Create MCP server
app = Server("dss-query-retrieve-agent")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available MCP tools.
    
    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="query_requirements",
            description=(
                "Query specifically about DICOM Store Service (DSS) requirements specification. "
                "Use this tool when you need information about functional requirements, business rules, use cases, "
                "constraints, or requirements documentation. This tool will give details "
                "about functional and non-functional requirements"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Your requirements-related question"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Optional session ID for conversation continuity",
                        "optional": True
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="query_design",
            description=(
                "Query the DICOM Store Service (DSS) system for design of features implemented in DICOM Store Service. "
                "This tool allows you to ask questions about the technical and low level design specifications of the DSS system."
                "Use this tool when the user asks about design or component interactions, or "
                "asks for explaining a feature in terms of design or architecture or implementation details or design documentation"
                "or when a user asks about tools or sdk used or any questions related to services."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Your design/architecture-related question"
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Optional session ID for conversation continuity",
                        "optional": True
                    }
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle MCP tool calls.
    
    Args:
        name: Tool name
        arguments: Tool arguments
        
    Returns:
        Tool response as TextContent
    """
    logger.info(f"Tool called: {name}")
    
    query = arguments.get("query", "")
    session_id = arguments.get("session_id")
    
    if not query:
        return [TextContent(type="text", text="Error: Query parameter is required")]
    
    try:
        # Add context based on tool type
        if name == "query_requirements":
            enhanced_query = f"Focus on requirements: {query}"
        elif name == "query_design":
            enhanced_query = f"Focus on design and architecture: {query}"
        else:
            enhanced_query = query
        
        logger.info(f"Invoking AgentCore with query: {enhanced_query[:100]}...")
        
        # Invoke agent synchronously (streaming handled by supervisor)
        # Note: The supervisor agent already streams responses internally
        response = await asyncio.to_thread(
            agentcore_client.invoke_agent,
            enhanced_query,
            session_id
        )
        
        logger.info(f"AgentCore response received ({len(response)} chars)")
        
        return [TextContent(type="text", text=response)]
        
    except Exception as e:
        error_msg = f"Error invoking agent: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return [TextContent(type="text", text=f"Error: {error_msg}")]

async def main():
    """Run the MCP server."""
    logger.info("Starting MCP server for DSS Query Retrieve Agent")
    logger.info(f"Agent Runtime ARN: {config.agent_runtime_arn}")
    logger.info(f"AWS Region: {config.aws_region}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
