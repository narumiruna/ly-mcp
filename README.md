# lyapi-mcp

### GitHub

```json
{
  "mcpServers": {
    "lyapimcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/lyapi-mcp",
        "lyapimcp"
      ]
    }
  }
}
```

### PyPI

```json
{
  "mcpServers": {
    "lyapimcp": {
      "command": "uvx",
      "args": ["lyapimcp@latest"]
    }
  }
}
```

### Local

```json
{
  "mcpServers": {
    "lyapimcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/lyapi-mcp",
        "lyapimcp"
      ]
    }
  }
}
```
