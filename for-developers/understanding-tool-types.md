---
description: >-
  UnifAI offers different ways to access and use tools in your agents. You can
  choose between dynamic discovery, static toolkits, or specific static actions
  based on your application's needs.
---

# 📙 Understanding Tool Types

### Dynamic Tools <a href="#dynamic-tools" id="dynamic-tools"></a>

Dynamic tools allow your agent to discover and use tools on-the-fly based on the context. This is the default behavior.

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
import { Tools } from 'unifai-sdk';

// Dynamic tools enabled by default
const tools = new Tools({ apiKey: 'YOUR_AGENT_API_KEY' });

// Or explicitly enable dynamic tools
const dynamicTools = await tools.getTools({ dynamicTools: true });
```
{% endtab %}

{% tab title="Python" %}
```
import unifai

# Dynamic tools enabled by default
tools = unifai.Tools(api_key='YOUR_AGENT_API_KEY')

# Or explicitly enable dynamic tools
dynamic_tools = await tools.get_tools(dynamic_tools=True) 
```
{% endtab %}

{% tab title="Rust" %}
```
use unifai_sdk::tools::get_tools;

// Dynamic tools enabled by default
let (search_tools, call_tool) = get_tools("YOUR_AGENT_API_KEY");
```
{% endtab %}
{% endtabs %}

**Benefits of dynamic tools:**

* Automatic discovery of relevant tools based on context
* Access to the full UnifAI tool ecosystem
* Tools are filtered to match the current user query
* New tools become available without code changes

### Static Toolkits <a href="#static-toolkits" id="static-toolkits"></a>

Static toolkits give you more control by specifying entire toolkits to be made available to your agent.

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
// Get tools from specific toolkits
const toolkitTools = await tools.getTools({
  dynamicTools: false,  // Optional: disable dynamic tools
  staticToolkits: ["toolkit_id_1", "toolkit_id_2"]
});
```
{% endtab %}

{% tab title="Python" %}
```
# Get tools from specific toolkits
toolkit_tools = await tools.get_tools(
    dynamic_tools=False,  // Optional: disable dynamic tools
    static_toolkits=["toolkit_id_1", "toolkit_id_2"]
)
```
{% endtab %}

{% tab title="Rust" %}
```
// Get tools from specific toolkits
let tools = get_static_toolkit_tools("YOUR_AGENT_API_KEY", vec!["toolkit_id_1", "toolkit_id_2"]);
```
{% endtab %}
{% endtabs %}

**Benefits of static toolkits:**

* Predictable set of available tools
* Reduced latency (no tool discovery needed)
* Full control over which toolkits your agent can access

### Static Actions <a href="#static-actions" id="static-actions"></a>

Static actions provide the most granular control, allowing you to specify individual actions (tools).

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
// Get specific actions
const actionTools = await tools.getTools({
  dynamicTools: false,  // Optional: disable dynamic tools
  staticActions: ["action_id_1", "action_id_2"]
});
```
{% endtab %}

{% tab title="Python" %}
```
# Get specific actions
action_tools = await tools.get_tools(
    dynamic_tools=False,  // Optional: disable dynamic tools
    static_actions=["action_id_1", "action_id_2"]
)
```
{% endtab %}

{% tab title="Rust" %}
```
// Get specific actions
let tools = get_static_action_tools("YOUR_AGENT_API_KEY", vec!["action_id_1", "action_id_2"]);
```
{% endtab %}
{% endtabs %}

**Benefits of static actions:**

* Maximum control over individual tools
* Minimal set of tools for specialized agents
* Ability to combine specific actions from different toolkits

### Combining Approaches <a href="#combining-approaches" id="combining-approaches"></a>

You can combine these approaches to create a customized tool setup:

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
// Combine dynamic and static tools
const combinedTools = await tools.getTools({
  dynamicTools: true,  // Enable dynamic discovery
  staticToolkits: ["essential_toolkit_id"],  // Always include this toolkit
  staticActions: ["critical_action_id"]  // Always include this specific action
});
```
{% endtab %}

{% tab title="Python" %}
```
# Combine dynamic and static tools
combined_tools = await tools.get_tools(
    dynamic_tools=True,  // Enable dynamic discovery
    static_toolkits=["essential_toolkit_id"],  // Always include this toolkit
    static_actions=["critical_action_id"]  // Always include this specific action
)
```
{% endtab %}

{% tab title="Rust" %}
```
// Combining approaches in Rust requires custom implementation
```
{% endtab %}
{% endtabs %}

This approach gives you the flexibility of dynamic discovery while ensuring that certain critical tools are always available to your agent.

### Caching Behavior <a href="#caching-behavior" id="caching-behavior"></a>

You can control the caching behavior of tool results:

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
// Enable cache control
const toolsWithCache = await tools.getTools({ cacheControl: true });
```
{% endtab %}

{% tab title="Python" %}
```
# Enable cache control
tools_with_cache = await tools.get_tools(cache_control=True)
```
{% endtab %}

{% tab title="Rust" %}
```
// Cache control in Rust requires custom implementation 
```
{% endtab %}
{% endtabs %}

When cache control is enabled, the LLM provider will treat tool results as ephemeral content that shouldn't be stored long-term.
