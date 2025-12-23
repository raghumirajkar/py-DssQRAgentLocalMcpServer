# Installation Guide for DSS AgentCore MCP Server

## For Team Members

### Option 1: Install from Local Directory (Recommended for Team Sharing)

1. **Get the package** from your teammate (zip file or shared drive)

2. **Extract** to a local directory (e.g., `C:\Temp\dss-agentcore-mcp`)

3. **Install** the package:
   ```powershell
   pip install C:\Temp\dss-agentcore-mcp
   ```

4. **Configure environment variables** (create `.env` file or set system variables):
   ```
   AGENTCORE_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU
   AWS_REGION=us-east-1
   ```

5. **Add to VS Code MCP config** (`%APPDATA%\Code\User\mcp.json`):
   ```json
   {
     "servers": {
       "dss-agentcore-mcp": {
         "type": "stdio",
         "command": "python",
         "args": ["-m", "dss_agentcore_mcp"],
         "env": {
           "AGENTCORE_RUNTIME_ARN": "arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU",
           "AWS_REGION": "us-east-1",
           "LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

6. **Restart VS Code**

### Option 2: Install from Git Repository (If you publish to GitHub)

```powershell
pip install git+https://github.com/yourusername/dss-agentcore-mcp.git
```

Then follow steps 4-6 from Option 1.

### Option 3: Install from PyPI (If you publish to PyPI)

```powershell
pip install dss-agentcore-mcp
```

Then follow steps 4-6 from Option 1.

## For Package Maintainers

### Building Distribution Package

1. **Install build tools**:
   ```powershell
   pip install build twine
   ```

2. **Build the package**:
   ```powershell
   cd C:\Views\Learning\DssQueryRetrieveAgentMcp
   python -m build
   ```
   
   This creates:
   - `dist/dss_agentcore_mcp-0.1.0-py3-none-any.whl` (wheel file)
   - `dist/dss_agentcore_mcp-0.1.0.tar.gz` (source distribution)

3. **Share with team**:
   - Share the entire directory (recommended for first-time setup)
   - OR share just the `.whl` file (teammates install with `pip install dss_agentcore_mcp-0.1.0-py3-none-any.whl`)
   - OR upload to private PyPI server

### Testing the Package Locally

```powershell
# Install in editable mode for development
pip install -e .

# Test running the server
python -m dss_agentcore_mcp

# Or test directly
python -c "from dss_agentcore_mcp import config; print(config.agent_runtime_arn)"
```

## Verifying Installation

After installation, verify it works:

```powershell
python -m dss_agentcore_mcp
```

You should see:
```
Starting MCP server for DSS Query Retrieve Agent
Agent Runtime ARN: arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU
AWS Region: us-east-1
```

## Troubleshooting

### "No module named 'dss_agentcore_mcp'"
- Package not installed. Run `pip install <path-to-package>`
- Check with `pip list | grep dss-agentcore-mcp`

### AWS Credentials Error
- Ensure AWS credentials are configured: `aws configure`
- Or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables

### Agent ARN Not Found
- Verify `AGENTCORE_RUNTIME_ARN` is set correctly
- Check the ARN format: `arn:aws:bedrock-agentcore:<region>:<account>:runtime/<name>-<id>`

### VS Code Not Detecting MCP Server
- Restart VS Code after adding to mcp.json
- Check VS Code Output panel > "GitHub Copilot" for errors
- Verify command: `python -m dss_agentcore_mcp` works in terminal
