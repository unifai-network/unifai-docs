---
description: >-
  UnifAI tools enable your agents to find and use tools dynamically. Below are
  code examples for initializing and using the tools. You will need an Agent API
  Key to use the tools, which you can get for
---

# 📒 Using Dynamic Tools in Your Agents

### Initializing Tools <a href="#initializing-tools" id="initializing-tools"></a>

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
import { Tools } from 'unifai-sdk';

const tools = new Tools({ apiKey: 'YOUR_AGENT_API_KEY' });
```
{% endtab %}

{% tab title="Python" %}
```
import unifai

tools = unifai.Tools(api_key='YOUR_AGENT_API_KEY')
```
{% endtab %}

{% tab title="Rust" %}
```
use unifai_sdk::tools::get_tools;

let (search_tools, call_tool) = get_tools("YOUR_AGENT_API_KEY");
```
{% endtab %}
{% endtabs %}

### Integrating with LLM <a href="#integrating-with-llm" id="integrating-with-llm"></a>

You can pass the initialized tools to any OpenAI-compatible API. For LLM that are not OpenAI compatible, you can use libraries and services such as [OpenRouter](https://openrouter.ai/docs) that gives you access to most LLMs through a single OpenAI compatible API.&#x20;

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
const messages = [{ content: "What is trending on Google today?", role: "user" }];
while (true) {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages,
    tools: await tools.getTools(),
  });
  messages.push(response.choices[0].message);
  const results = await tools.callTools(response.choices[0].message.tool_calls);
  if (results.length === 0) break;
  messages.push(...results);
}
```
{% endtab %}

{% tab title="Python" %}
```
messages = [{"content": "What is trending on Google today?", "role": "user"}]
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=await tools.get_tools(),
    )
    messages.append(response.choices[0].message)
    results = await tools.call_tools(response.choices[0].message.tool_calls)
    if len(results) == 0:
        break
    messages.extend(results)
```
{% endtab %}

{% tab title="Rust" %}
```
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
{% endtab %}
{% endtabs %}

### System Prompt <a href="#system-prompt" id="system-prompt"></a>

Most models are good at searching and using UnifAI tools without any special instructions. But we find using a system prompt helps the model to search and use the tools more effectively.

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
