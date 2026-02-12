# Quick Start Guide - Running the Agent with Loki Integration

## Prerequisites

✅ Docker installed and running  
✅ Loki MCP server Docker image available  
✅ Loki instance accessible at `http://192.168.1.100:3100`

## Step-by-Step Startup

### 1. Start the Loki MCP Server

```bash
cd /Users/kanishqk77/Desktop/do-anything-repo/agent
docker-compose up -d
```

**Verify the container is running:**
```bash
docker ps | grep loki-mcp-server
```

Expected output:
```
CONTAINER ID   IMAGE             COMMAND   CREATED   STATUS   PORTS                    NAMES
...            loki-mcp-server   ...       ...       Up       0.0.0.0:8081->8080/tcp   loki-mcp-server
```

### 2. Run the ADK Agent

```bash
cd /Users/kanishqk77/Desktop/do-anything-repo/agent
adk run root_agent
```

The agent will start with:
- ✅ Root Agent (main entry point)
- ✅ Prometheus Agent (metrics on port 8080)
- ✅ Loki Agent (logs on port 8081)
- ✅ Langfuse Observability enabled

### 3. Test the Integration

Once the ADK agent is running, you can ask questions like:

**For Loki/Logs:**
- "Show me recent error logs"
- "Query Loki for authentication failures"
- "What's happening in the application logs?"

**For Prometheus/Metrics:**
- "What's the current CPU usage?"
- "Show me memory consumption metrics"
- "Get the list of Prometheus targets"

## Stopping Services

```bash
# Stop the agent (Ctrl+C in the terminal)

# Stop Loki MCP server
docker-compose down
```

## Troubleshooting

### Loki MCP Server Not Starting

```bash
# Check logs
docker logs loki-mcp-server

# Check if Loki is accessible from the container
docker exec loki-mcp-server curl http://192.168.1.100:3100/ready
```

### Port Already in Use

If port 8081 is in use, edit `docker-compose.yml`:

```yaml
ports:
  - "8082:8080"  # Change to available port
```

And update `.env`:
```
LOKI_MCP_URL=http://localhost:8082/sse
```

### Agent Can't Connect to MCP Server

Ensure the MCP server is running and accessible:
```bash
curl http://localhost:8081/sse
```

## Architecture Overview

See the complete architecture documentation:
- **Full Diagrams:** `/Users/kanishqk77/.gemini/antigravity/brain/43f1793b-547e-4fb0-b19d-eb31df570bdb/architecture_diagram.md`
- **Loki Details:** `README_LOKI.md`

---

**🎉 You're all set!** Your agent now has both Prometheus metrics and Loki log analysis capabilities.
