# DSS Query Retrieve Agent - MCP Server

Thin local MCP server that provides VS Code integration with the deployed AWS AgentCore Supervisor Agent.

## Architecture

```
GitHub Copilot/Claude in VS Code
    |
    | (MCP stdio transport)
    v
Local MCP Server (this project)
    |
    | (boto3 InvokeAgentRuntime)
    v
Supervisor Agent (AWS AgentCore)
    |
    |-- Requirements Analyzer Tool
    |-- Design Analyzer Tool
    v
Response Synthesis
```

## Setup

### 1. Install Dependencies

```powershell
cd C:\Views\Learning\DssQueryRetrieveAgentMcp
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

Copy `.env.example` to `.env` and customize if needed:

```powershell
copy .env.example .env
```

Default configuration:
- **Agent Runtime ARN**: `arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU`
- **AWS Region**: `us-east-1`
- **Log Level**: `INFO`

### 3. AWS Credentials

Ensure AWS credentials are configured:
- Use AWS CLI: `aws configure`
- Or set environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Or use IAM roles (if running on EC2/ECS)

### 4. Test the Server

Run locally to test:

```powershell
python mcp_server.py
```

Press Ctrl+C to stop.

## VS Code Integration

Add to your VS Code MCP configuration file (`%APPDATA%\Code\User\mcp.json`):

```json
{
  "mcpServers": {
    "dss-query-retrieve-agent": {
      "command": "C:\\Views\\Learning\\DssQueryRetrieveAgentMcp\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Views\\Learning\\DssQueryRetrieveAgentMcp\\mcp_server.py"
      ],
      "env": {
        "AGENTCORE_RUNTIME_ARN": "arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

**Note**: Update paths if your Python virtual environment is in a different location.

## Available MCP Tools

### 1. `query_dss`
General query tool that automatically routes to appropriate analyzers.

**Use for**: Any question about DSS - requirements, design, or general information.

**Example**:
```
Query: "What are the requirements for study complete notification?"
```

### 2. `query_requirements`
Specifically queries requirements documentation.

**Use for**: Requirements, business rules, use cases, constraints.

**Example**:
```
Query: "What are the auditing requirements?"
```

### 3. `query_design`
Specifically queries design and architecture documentation.

**Use for**: System architecture, design patterns, technical specifications.

**Example**:
```
Query: "Explain the logging framework design"
```

## Usage in VS Code

1. Open VS Code
2. Use GitHub Copilot Chat or Claude
3. Reference the MCP tools using `@dss-query-retrieve-agent`
4. Ask your questions naturally

**Example prompts**:
- `@dss-query-retrieve-agent query the requirements for image storage`
- `@dss-query-retrieve-agent what is the design of the notification system?`

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENTCORE_RUNTIME_ARN` | AWS AgentCore agent runtime ARN | Required |
| `AWS_REGION` | AWS region | `us-east-1` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

### Updating Agent ARN

If you redeploy the supervisor agent and get a new ARN:

1. Update in `mcp.json` env section
2. Or update `.env` file
3. Or update default in `config.py`

Restart VS Code after updating.

## Troubleshooting

### MCP Server Not Starting

Check logs in VS Code Developer Tools:
- Help → Toggle Developer Tools → Console

### AWS Permission Errors

Ensure your AWS credentials have permissions:
- `bedrock-agentcore:InvokeAgentRuntime`

### Agent Not Responding

Verify:
1. Agent is deployed: `agentcore list`
2. Agent ARN is correct
3. AWS region matches deployment region

## Development

### Testing Locally

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run server
python mcp_server.py

# Server will wait for stdio input (MCP protocol)
# Press Ctrl+C to exit
```

### Viewing Logs

Set `LOG_LEVEL=DEBUG` in environment to see detailed logs.

## Project Structure

```
DssQueryRetrieveAgentMcp/
├── mcp_server.py          # MCP server implementation
├── agentcore_client.py    # AWS AgentCore client wrapper
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## License

Internal use only.
