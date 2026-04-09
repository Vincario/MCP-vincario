# Vincario MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that exposes the
[Vincario API](https://vincario.com/) to AI agents and LLM clients. Enables AI assistants to
decode VINs, check stolen vehicle databases, and retrieve market valuations through natural language.

## Tools

| Tool | Description |
|---|---|
| `vin_decode` | Decode a VIN and return detailed vehicle information |
| `vin_decode_info` | List available fields for a given VIN (free endpoint) |
| `stolen_check` | Check if a VIN appears in stolen vehicle databases |
| `vehicle_market_value` | Get market valuation for a vehicle (supports odometer input) |

## Requirements

- [Vincario API key](https://vincario.com/vin-decoder/) — passed via `X-API-Key` HTTP header
- Docker (recommended), or Python 3.11+ with [uv](https://github.com/astral-sh/uv)

## Running with Docker

```bash
docker build -t vincario-mcp .
docker run -p 8080:8080 vincario-mcp
```

The server starts on `http://localhost:8080`.

## Running locally

```bash
pip install uv
uv sync
uv run main.py
```

## Connecting to an MCP client

Pass your Vincario API key as an HTTP header with each request:

```
X-API-Key: your_api_key_here
```

### Claude Code

Add to your MCP config (`.mcp.json` or `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "vincario": {
      "type": "http",
      "url": "http://localhost:8080",
      "headers": {
        "X-API-Key": "your_api_key_here"
      }
    }
  }
}
```

### Hosted endpoint

If connecting to the hosted server at `https://mcp.vincario.com/mcp`, replace the URL accordingly.

## Example usage

Once connected, you can ask your AI assistant:

- *"Decode VIN WBAFR9C54BC780006"*
- *"Is this vehicle stolen? VIN: WBAFR9C54BC780006"*
- *"What is the market value of VIN WBAFR9C54BC780006 with 85000 km?"*

## Transport

The server uses **streamable HTTP** transport (`stateless_http=True`), which means no persistent session is required. Each request is independent, making it straightforward to deploy behind a reverse proxy or load balancer.

For HTTPS deployment, place a reverse proxy (nginx, Caddy, Cloudflare) in front of the server — the application itself runs on plain HTTP port 8080.

## License

See [Vincario API Terms of Service](https://vincario.com/terms-and-conditions/) for usage terms.
