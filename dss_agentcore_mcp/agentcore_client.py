"""AWS AgentCore Runtime client wrapper."""

import json
import logging
import uuid
from typing import Iterator, Optional

import boto3
from botocore.exceptions import ClientError

from .config import config

logger = logging.getLogger(__name__)


class AgentCoreClient:
    """Client for interacting with AWS AgentCore Runtime."""
    
    def __init__(self, runtime_arn: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize AgentCore client.
        
        Args:
            runtime_arn: Agent runtime ARN (uses config default if not provided)
            region: AWS region (uses config default if not provided)
        """
        self.runtime_arn = runtime_arn or config.agent_runtime_arn
        self.region = region or config.aws_region
        
        self.client = boto3.client('bedrock-agentcore', region_name=self.region)
        
        logger.info(f"AgentCore client initialized")
        logger.info(f"Runtime ARN: {self.runtime_arn}")
        logger.info(f"Region: {self.region}")
    
    def invoke_agent(self, prompt: str, session_id: Optional[str] = None) -> str:
        """
        Invoke the deployed supervisor agent synchronously.
        
        Args:
            prompt: User prompt to send to the agent
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Complete response from the agent
            
        Raises:
            Exception: If invocation fails
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        logger.info(f"Invoking agent (session: {session_id[:8]}...)")
        
        try:
            # Prepare payload
            payload = json.dumps({"prompt": prompt}).encode('utf-8')
            
            # Invoke agent
            response = self.client.invoke_agent_runtime(
                agentRuntimeArn=self.runtime_arn,
                runtimeSessionId=session_id,
                payload=payload
            )
            
            # Read response
            if 'response' in response:
                response_stream = response['response']
                if hasattr(response_stream, 'read'):
                    result = response_stream.read().decode('utf-8')
                else:
                    # Handle streaming response
                    result_parts = []
                    for event in response_stream:
                        if isinstance(event, bytes):
                            result_parts.append(event.decode('utf-8'))
                        elif isinstance(event, dict):
                            if 'chunk' in event:
                                result_parts.append(event['chunk'].get('bytes', b'').decode('utf-8'))
                    result = ''.join(result_parts)
            else:
                result = ""
            
            logger.info(f"Agent response received ({len(result)} chars)")
            return result
            
        except ClientError as e:
            logger.error(f"AgentCore invocation failed: {e}")
            raise Exception(f"Failed to invoke agent: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise
    
    def invoke_agent_stream(self, prompt: str, session_id: Optional[str] = None) -> Iterator[str]:
        """
        Invoke the deployed supervisor agent with streaming response.
        
        Args:
            prompt: User prompt to send to the agent
            session_id: Optional session ID for conversation continuity
            
        Yields:
            Response chunks from the agent
            
        Raises:
            Exception: If invocation fails
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        logger.info(f"Invoking agent with streaming (session: {session_id[:8]}...)")
        
        try:
            # Prepare payload
            payload = json.dumps({"prompt": prompt}).encode('utf-8')
            
            # Invoke agent
            response = self.client.invoke_agent_runtime(
                agentRuntimeArn=self.runtime_arn,
                runtimeSessionId=session_id,
                payload=payload
            )
            
            # Stream response
            if 'response' in response:
                response_stream = response['response']
                
                if hasattr(response_stream, 'read'):
                    # Non-streaming response
                    yield response_stream.read().decode('utf-8')
                else:
                    # Streaming response
                    for event in response_stream:
                        if isinstance(event, bytes):
                            chunk = event.decode('utf-8')
                            logger.debug(f"Streaming chunk: {len(chunk)} chars")
                            yield chunk
                        elif isinstance(event, dict):
                            if 'chunk' in event:
                                chunk = event['chunk'].get('bytes', b'').decode('utf-8')
                                logger.debug(f"Streaming chunk: {len(chunk)} chars")
                                yield chunk
            
            logger.info("Streaming completed")
            
        except ClientError as e:
            logger.error(f"AgentCore streaming invocation failed: {e}")
            raise Exception(f"Failed to invoke agent with streaming: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during streaming: {e}", exc_info=True)
            raise
