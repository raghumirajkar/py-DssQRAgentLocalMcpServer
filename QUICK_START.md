# Quick Start - Install & Use DSS AgentCore MCP Server

## ✅ Package Successfully Built!

Distribution files created in `dist/`:
- `dss_agentcore_mcp-0.1.0-py3-none-any.whl` (wheel file - recommended)
- `dss_agentcore_mcp-0.1.0.tar.gz` (source distribution)

---

## 🚀 Installation Steps

### Option 1: Install from Wheel (Recommended)

```powershell
pip install C:\Views\Learning\DssQueryRetrieveAgentMcp\dist\dss_agentcore_mcp-0.1.0-py3-none-any.whl
```

### Option 2: Install from Source

```powershell
pip install C:\Views\Learning\DssQueryRetrieveAgentMcp\dist\dss_agentcore_mcp-0.1.0.tar.gz
```

### Option 3: Install in Editable Mode (For Development)

```powershell
pip install -e C:\Views\Learning\DssQueryRetrieveAgentMcp
```

---

## 📋 VS Code MCP Configuration

After installation, add this to `%APPDATA%\Code\User\mcp.json`:

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

**Key differences from your azure_mcp example:**
- Uses `python -m dss_agentcore_mcp` (same pattern as `python -m azure_devops_mcp`)
- Environment variables specific to AgentCore (ARN, AWS region)
- No need for tokens/passwords - uses AWS credentials from environment

---

## 🧪 Test the Installation

### 1. Verify package is installed:
```powershell
pip list | Select-String "dss-agentcore-mcp"
```

### 2. Test running the server:
```powershell
python -m dss_agentcore_mcp
```

You should see:
```
Starting MCP server for DSS Query Retrieve Agent
Agent Runtime ARN: arn:aws:bedrock-agentcore:us-east-1:519677643490:runtime/dss_query_retrieve_agent-UO4Mf76GpU
AWS Region: us-east-1
```

Press `Ctrl+C` to stop.

### 3. Test from VS Code:
- Restart VS Code after adding to mcp.json
- In chat, ask: `@dss-agentcore-mcp what are the requirements for auditing?`

---

## 📦 Share with Teammates

### Method 1: Share Wheel File (Easiest)

1. **Share the file**: `dist\dss_agentcore_mcp-0.1.0-py3-none-any.whl`

2. **Teammates install**:
   ```powershell
   pip install dss_agentcore_mcp-0.1.0-py3-none-any.whl
   ```

3. **Teammates configure VS Code** (see mcp.json above)

### Method 2: Share Entire Project Folder

1. **Zip the project folder** (exclude `venv/`, `__pycache__/`, `.env`)

2. **Teammates extract and install**:
   ```powershell
   pip install C:\path\to\DssQueryRetrieveAgentMcp
   ```

### Method 3: Internal Git Repository

```powershell
# You: Push to Git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://your-git-server/dss-agentcore-mcp.git
git push -u origin main

# Teammates: Install from Git
pip install git+https://your-git-server/dss-agentcore-mcp.git
```

---

## ⚙️ Configuration Options

### Environment Variables (in mcp.json or .env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AGENTCORE_RUNTIME_ARN` | ✅ Yes | (provided) | ARN of deployed agent |
| `AWS_REGION` | No | `us-east-1` | AWS region |
| `LOG_LEVEL` | No | `INFO` | Log verbosity |

### AWS Credentials

Ensure AWS credentials are configured:
```powershell
aws configure
```

Or set environment variables:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (if using temporary credentials)

---

## 🆚 Comparison with azure_mcp

| Aspect | azure_mcp | dss-agentcore-mcp |
|--------|-----------|-------------------|
| **Command** | `python -m azure_devops_mcp` | `python -m dss_agentcore_mcp` |
| **Auth** | Token in env vars | AWS credentials |
| **Config** | Azure DevOps URL, Org, Project | AgentCore ARN, AWS Region |
| **Transport** | stdio | stdio |
| **Pattern** | ✅ Same! | ✅ Same! |

---

## 🔧 Troubleshooting

### "No module named 'dss_agentcore_mcp'"
- Run: `pip install dist\dss_agentcore_mcp-0.1.0-py3-none-any.whl`
- Verify: `pip list | Select-String "dss"`

### AWS Credentials Error
- Run: `aws configure`
- Or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### VS Code Not Detecting Server
- Restart VS Code completely
- Check: Output panel > "GitHub Copilot" for errors
- Test manually: `python -m dss_agentcore_mcp` should run without errors

### Agent ARN Not Found
- Verify ARN is correct in mcp.json
- Check AWS region matches where agent is deployed
- Test with AWS CLI: `aws bedrock-agent-runtime invoke-agent` (if available)

---

## 📚 Additional Documentation

- [INSTALL.md](INSTALL.md) - Detailed installation instructions
- [README.md](README.md) - Architecture and development guide
- [.env.example](.env.example) - Environment variable template
