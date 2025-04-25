---
sidebar_position: 7
title: Tool Types
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Understanding Tool Types

UnifAI offers different ways to access and use tools in your agents. You can choose between dynamic discovery, static toolkits, or specific static actions based on your application's needs.

## Dynamic Tools

Dynamic tools allow your agent to discover and use tools on-the-fly based on the context. This is the default behavior.

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
import { Tools } from 'unifai-sdk';

// Dynamic tools enabled by default
const tools = new Tools({ apiKey: 'YOUR_AGENT_API_KEY' });

// Or explicitly enable dynamic tools
const dynamicTools = tools.getTools({ dynamicTools: true });
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
import unifai

# Dynamic tools enabled by default
tools = unifai.Tools(api_key='YOUR_AGENT_API_KEY')

# Or explicitly enable dynamic tools
dynamic_tools = tools.get_tools(dynamicTools=True)
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
use unifai_sdk::tools::get_tools;

// Dynamic tools enabled by default
let (search_tools, call_tool) = get_tools("YOUR_AGENT_API_KEY");
```

  </TabItem>
</Tabs>

**Benefits of dynamic tools:**
- Automatic discovery of relevant tools based on context
- Access to the full UnifAI tool ecosystem
- Tools are filtered to match the current user query
- New tools become available without code changes

## Static Toolkits

Static toolkits give you more control by specifying entire toolkits to be made available to your agent.

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
// Get tools from specific toolkits
const toolkitTools = tools.getTools({
  dynamicTools: false,  // Optional: disable dynamic tools
  staticToolkits: ["toolkit_id_1", "toolkit_id_2"]
});
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
# Get tools from specific toolkits
toolkit_tools = tools.get_tools(
    dynamicTools=False,  # Optional: disable dynamic tools
    staticToolkits=["toolkit_id_1", "toolkit_id_2"]
)
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
// Get tools from specific toolkits
let tools = get_static_toolkit_tools("YOUR_AGENT_API_KEY", vec!["toolkit_id_1", "toolkit_id_2"]);
```

  </TabItem>
</Tabs>

**Benefits of static toolkits:**
- Predictable set of available tools
- Reduced latency (no tool discovery needed)
- Full control over which toolkits your agent can access

## Static Actions

Static actions provide the most granular control, allowing you to specify individual actions (tools).

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
// Get specific actions
const actionTools = tools.getTools({
  dynamicTools: false,  // Optional: disable dynamic tools
  staticActions: ["action_id_1", "action_id_2"]
});
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
# Get specific actions
action_tools = tools.get_tools(
    dynamicTools=False,  # Optional: disable dynamic tools
    staticActions=["action_id_1", "action_id_2"]
)
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
// Get specific actions
let tools = get_static_action_tools("YOUR_AGENT_API_KEY", vec!["action_id_1", "action_id_2"]);
```

  </TabItem>
</Tabs>

**Benefits of static actions:**
- Maximum control over individual tools
- Minimal set of tools for specialized agents
- Ability to combine specific actions from different toolkits

## Combining Approaches

You can combine these approaches to create a customized tool setup:

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
// Combine dynamic and static tools
const combinedTools = tools.getTools({
  dynamicTools: true,  // Enable dynamic discovery
  staticToolkits: ["essential_toolkit_id"],  // Always include this toolkit
  staticActions: ["critical_action_id"]  // Always include this specific action
});
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
# Combine dynamic and static tools
combined_tools = tools.get_tools(
    dynamicTools=True,  # Enable dynamic discovery
    staticToolkits=["essential_toolkit_id"],  # Always include this toolkit
    staticActions=["critical_action_id"]  # Always include this specific action
)
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
// Combining approaches in Rust requires custom implementation
```

  </TabItem>
</Tabs>

This approach gives you the flexibility of dynamic discovery while ensuring that certain critical tools are always available to your agent.

## Caching Behavior

You can control the caching behavior of tool results:

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
// Enable cache control
const toolsWithCache = tools.getTools({ cacheControl: true });
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
# Enable cache control
tools_with_cache = tools.get_tools(cache_control=True)
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
// Cache control in Rust requires custom implementation
```

  </TabItem>
</Tabs>

When cache control is enabled, the LLM provider will treat tool results as ephemeral content that shouldn't be stored long-term.