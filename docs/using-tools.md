---
sidebar_position: 3
title: Using Tools in Your Agents
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Using Dynamic Tools in Your Agents

UnifAI tools enable your agents to find and use tools dynamically. Below are code examples for initializing and using the tools. You will need an **Agent API Key** to use the tools — which you can get for free from [UnifAI](https://app.unifai.network/).

## Initializing Tools

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
import { Tools } from 'unifai-sdk';

const tools = new Tools({ apiKey: 'YOUR_AGENT_API_KEY' });
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
import unifai

tools = unifai.Tools(api_key='YOUR_AGENT_API_KEY')
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
use unifai_sdk::tools::get_tools;

let (search_tools, call_tool) = get_tools("YOUR_AGENT_API_KEY");
```

  </TabItem>
</Tabs>

## Integrating with LLM

You can pass the initialized tools to any OpenAI-compatible API.
For LLM that are not OpenAI compatible, you can use libraries and services such as [OpenRouter](https://openrouter.ai/docs) that gives you access to most LLMs through a single OpenAI compatible API.

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
const messages = [{ content: "What is trending on Google today?", role: "user" }];
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages,
  tools: tools.getTools(),
});
messages.push(response.choices[0].message);
if (response.choices[0].message.tool_calls) {
  const results = await tools.callTools(response.choices[0].message.tool_calls);
  messages.push(...results);
  // messages can be passed to the LLM again now
}
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
messages = [{"content": "What is trending on Google today?", "role": "user"}]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools.get_tools(),
)
messages.append(response.choices[0].message)
if response.choices[0].message.get("tool_calls"):
    results = await tools.call_tools(response.choices[0].message["tool_calls"])
    messages.extend(results)
    # messages can be passed to the LLM again now
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
let agent = openai_client
    .agent("gpt-4o")
    .tool(search_tools)
    .tool(call_tool)
    .build();
let result = agent
    .prompt("What is trending on Google today?")
    .await
    .unwrap();
```

  </TabItem>
</Tabs>

Passing the tool calls results back to the LLM might get you more function calls, and you can keep calling the tools until you get a response that doesn't contain any tool calls. For example:

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```javascript
const messages = [{ content: "What is trending on Google today?", role: "user" }];
while (true) {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages,
    tools: tools.getTools(),
  });
  messages.push(response.choices[0].message);
  const results = await tools.callTools(response.choices[0].message.tool_calls);
  if (results.length === 0) break;
  messages.push(...results);
}
```

  </TabItem>
  <TabItem value="py" label="Python">

```python
messages = [{"content": "What is trending on Google today?", "role": "user"}]
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools.get_tools(),
    )
    messages.append(response.choices[0].message)
    results = await tools.call_tools(response.choices[0].message.tool_calls)
    if len(results) == 0:
        break
    messages.extend(results)
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```rust
let mut messages = vec![Message::user("What is trending on Google today?")];
let result = loop {
    let response = agent
        .completion("", messages.clone())
        .await
        .unwrap()
        .send()
        .await
        .unwrap();
    let content = response.choice.first();
    messages.push(Message::Assistant {
        content: OneOrMany::one(content.clone()),
    });
    match content {
        AssistantContent::Text(text) => {
            break text;
        }
        AssistantContent::ToolCall(tool_call) => {
            let tool_result = agent
                .tools
                .call(
                    &tool_call.function.name,
                    tool_call.function.arguments.to_string(),
                )
                .await
                .unwrap();
            chat_history.push(Message::User {
                content: OneOrMany::one(UserContent::ToolResult(ToolResult {
                    id: tool_call.id,
                    content: OneOrMany::one(ToolResultContent::Text(Text {
                        text: tool_result,
                    })),
                })),
            })
        }
    }
};
```

  </TabItem>
</Tabs>

## System Prompt

Most models are good at searching and using UnifAI tools without any special instructions.
But we find using a system prompt helps the model to search and use the tools more effectively.

An example system prompt:

```
You are an intelligent personal assistant with access to various services to help accomplish tasks.
When given a task that you cannot complete immediately (due to missing information or required actions),
identify and utilize appropriate services to help solve it.

# SERVICE SEARCH GUIDELINES
When searching for services:
- Focus on relevant generic keywords rather than specific details
- Think about the category or type of service needed
- If initial search fails, refine your query and try again
- Search for one service at a time. Each search only gives you services relevant to your query, so do not try to search for multiple services in one call.

# SERVICE USAGE GUIDELINES
Before using any service:
- Explain to the user which services you found from the search
- Justify your service selection
- Proceed with the service execution

# IMPORTANT RULES
- Actions returned by search_services must ONLY be used in invoke_service function as payload, they are NOT functions that can be called directly.
```
