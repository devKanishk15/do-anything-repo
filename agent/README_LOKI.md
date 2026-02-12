# Loki MCP Server Integration

This document explains how to run and use the Loki MCP server integration with the Google ADK agent.

## Prerequisites

- Docker installed and running
- Loki MCP server Docker image built or available
- Loki instance accessible at `http://192.168.1.100:3100` (or update the URL in `.env` and `docker-compose.yml`)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Start the Loki MCP server:**
   ```bash
   docker-compose up -d
   ```

2. **Verify the container is running:**
   ```bash
   docker ps | grep loki-mcp-server
   ```

3. **Check logs:**
   ```bash
   docker logs loki-mcp-server
   ```

4. **Stop the server:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker CLI Directly

Run the Loki MCP server using the original command (modified for port 8081 to avoid conflicts):

```bash
docker run -d \
  --name loki-mcp-server \
  -e LOKI_URL="http://192.168.1.100:3100" \
  -p 8081:8080 \
  loki-mcp-server
```

**Note:** We're using port `8081` on the host to avoid conflicts with the Prometheus MCP server on port `8080`.

## Configuration

### Environment Variables

The Loki agent is configured via the `.env` file in `hello_agent/`:

- `LOKI_MCP_URL`: The SSE endpoint for the Loki MCP server (defaults to `http://localhost:8081/sse`)
- `LOKI_URL`: The URL of your Grafana Loki instance (set via Docker environment variable)

### Updating Loki URL

If your Loki instance is at a different URL:

1. Update the `LOKI_URL` in `docker-compose.yml`
2. Or set it when running with Docker CLI:
   ```bash
   docker run -d --name loki-mcp-server -e LOKI_URL="http://your-loki-url:3100" -p 8081:8080 loki-mcp-server
   ```

## Agent Usage

The Loki agent is automatically integrated into the root agent. You can ask questions about logs:

- "Show me error logs from the last hour"
- "Query Loki for application logs with status 500"
- "What errors occurred in the auth service?"

The Loki agent will use LogQL queries to fetch and analyze your log data.

## Troubleshooting

### Connection Issues

1. **Verify the container is running:**
   ```bash
   docker ps | grep loki-mcp-server
   ```

2. **Check container logs:**
   ```bash
   docker logs loki-mcp-server
   ```

3. **Test the MCP server endpoint:**
   ```bash
   curl http://localhost:8081/sse
   ```

4. **Verify Loki connectivity from the container:**
   ```bash
   docker exec loki-mcp-server curl http://192.168.1.100:3100/ready
   ```

### Port Conflicts

If port 8081 is already in use, you can change it:

1. Update `docker-compose.yml` to use a different port (e.g., `8082:8080`)
2. Update `LOKI_MCP_URL` in `.env` accordingly (e.g., `http://localhost:8082/sse`)

### Rebuilding the Container

If you need to rebuild the Loki MCP server image:

```bash
# Stop and remove existing container
docker stop loki-mcp-server
docker rm loki-mcp-server

# Rebuild the image (from your Loki MCP server source directory)
docker build -t loki-mcp-server .

# Start again with docker-compose
docker-compose up -d
```

## Architecture

```
┌─────────────────────┐
│   Root Agent        │
│                     │
│  ┌──────────────┐   │
│  │ Loki Agent   │   │
│  │              │   │
│  │ MCPToolset   │   │
│  └──────┬───────┘   │
└─────────┼───────────┘
          │ SSE
          ▼
┌─────────────────────┐
│ Loki MCP Server     │
│ (Docker Container)  │
│ Port: 8081          │
└─────────┬───────────┘
          │ HTTP
          ▼
┌─────────────────────┐
│ Grafana Loki        │
│ 192.168.1.100:3100  │
└─────────────────────┘
```

## Next Steps

- Customize the `loki_agent.py` instruction to match your specific use case
- Add more MCP tools to the `tool_filter` list as they become available
- Integrate additional log sources or queries
