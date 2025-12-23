"""Configuration for MCP server and AWS AgentCore client."""

import os
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration for the MCP server."""
    
    # AWS AgentCore Configuration
    agent_runtime_arn: str = os.getenv(
        'AGENTCORE_RUNTIME_ARN',
        'arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU'
    )
    aws_region: str = os.getenv('AWS_REGION', 'us-east-1')
    
    # Logging Configuration
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    def __post_init__(self):
        """Validate configuration."""
        if not self.agent_runtime_arn:
            raise ValueError("AGENTCORE_RUNTIME_ARN must be set")
        if not self.aws_region:
            raise ValueError("AWS_REGION must be set")

# Global config instance
config = Config()
