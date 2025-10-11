---
description: >-
  UnifAI SDK provides an MCP (Model Context Protocol) server that can be used
  with MCP-compatible clients like Claude Desktop.
---

# 📗 Using Dynamic Tools in MCP Clients

### Setting Up the MCP Server <a href="#setting-up-the-mcp-server" id="setting-up-the-mcp-server"></a>

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
{
  "mcpServers": {
    "unifai": {
      "command": "npx",
      "args": [
        "-y",
        "-p",
        "unifai-sdk",
        "unifai-tools-mcp"
      ],
      "env": {
        "UNIFAI_AGENT_API_KEY": "YOUR_AGENT_API_KEY"
      }
    }
  }
}
```
{% endtab %}

{% tab title="Python" %}
```
{
  "mcpServers": {
    "unifai": {
      "command": "uvx",
      "args": [
        "--from",
        "unifai-sdk",
        "unifai-tools-mcp"
      ],
      "env": {
        "UNIFAI_AGENT_API_KEY": "YOUR_AGENT_API_KEY"
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Configuration Steps <a href="#configuration-steps" id="configuration-steps"></a>

1. Install `npm` (for JavaScript/TypeScript) or `uvx` (for Python) following the official installation instructions.
2. Update your MCP client configuration (for example, in Claude Desktop) with the JSON configuration above.
3. Make sure you put your agent API key in the configuration file.

### Configuring Tool Types <a href="#configuring-tool-types" id="configuring-tool-types"></a>

You can use environment variables to control which tools are exposed by the MCP server:

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
{
  "mcpServers": {
    "unifai": {
      "command": "npx",
      "args": [
        "-y",
        "-p",
        "unifai-sdk",
        "unifai-tools-mcp"
      ],
      "env": {
        "UNIFAI_AGENT_API_KEY": "YOUR_AGENT_API_KEY",
        "UNIFAI_DYNAMIC_TOOLS": "true",
        "UNIFAI_STATIC_TOOLKITS": "1,2,3",
        "UNIFAI_STATIC_ACTIONS": "ACTION_A,ACTION_B"
      }
    }
  }
}
```
{% endtab %}

{% tab title="Python" %}
```
{
  "mcpServers": {
    "unifai": {
      "command": "uvx",
      "args": [
        "--from",
        "unifai-sdk",
        "unifai-tools-mcp"
      ],
      "env": {
        "UNIFAI_AGENT_API_KEY": "YOUR_AGENT_API_KEY",
        "UNIFAI_DYNAMIC_TOOLS": "true",
        "UNIFAI_STATIC_TOOLKITS": "1,2,3",
        "UNIFAI_STATIC_ACTIONS": "ACTION_A,ACTION_B"
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

The environment variables control the tool discovery behavior:

* `UNIFAI_DYNAMIC_TOOLS`: Set to "true" to enable dynamic tool discovery (default)
* `UNIFAI_STATIC_TOOLKITS`: Comma-separated list of toolkit IDs to include
* `UNIFAI_STATIC_ACTIONS`: Comma-separated list of action IDs to include

Once configured, your MCP client will detect and utilize the tools exposed by your toolkit.
