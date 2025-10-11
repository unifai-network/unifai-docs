---
description: >-
  Toolkits allow you to make tools available to all UnifAI agents as a service.
  This section shows you how to create, configure, and run your toolkits using
  both the JavaScript/TypeScript and Python SDK
---

# 📔 Creating Toolkits

### Overview <a href="#overview" id="overview"></a>

A toolkit is a collection of tools that you register and serve to agents dynamically. It requires a **Toolkit API Key** — which you can get for free from [UnifAI](https://app.unifai.network/).

### Toolkit Creation and Configuration <a href="#toolkit-creation-and-configuration" id="toolkit-creation-and-configuration"></a>

Let's break down the process of creating and configuring a toolkit:

#### Initialize the Toolkit <a href="#initialize-the-toolkit" id="initialize-the-toolkit"></a>

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
import { Toolkit } from 'unifai-sdk';

const toolkit = new Toolkit({ apiKey: 'YOUR_TOOLKIT_API_KEY' });
```
{% endtab %}

{% tab title="Python" %}
```
import unifai

toolkit = unifai.Toolkit(api_key='YOUR_TOOLKIT_API_KEY')
```
{% endtab %}

{% tab title="Rust" %}
```
use unifai_sdk::toolkit::*;

let mut toolkit = ToolkitService::new("YOUR_TOOLKIT_API_KEY");
```
{% endtab %}
{% endtabs %}

#### Update Toolkit Details <a href="#update-toolkit-details" id="update-toolkit-details"></a>

You can optionally update the toolkit's name and description:

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
await toolkit.updateToolkit({ 
    name: "EchoChamber", 
    description: "What's in, what's out." 
});
```
{% endtab %}

{% tab title="Python" %}
```
await toolkit.update_toolkit(
    name="EchoChamber",
    description="What's in, what's out."
)

# Or using asyncio.run():
# asyncio.run(toolkit.update_toolkit(name="EchoChamber", description="What's in, what's out."))
```
{% endtab %}

{% tab title="Rust" %}
```
service
    .update_info(ToolkitInfo {
        name: "EchoChamber".to_string(),
        description: "What's in, what's out.".to_string(),
    })
    .await
    .unwrap();
```
{% endtab %}
{% endtabs %}

#### Register Action Handlers <a href="#register-action-handlers" id="register-action-handlers"></a>

Register actions that your toolkit will provide. The `payloadDescription` can be any string or dictionary that contains enough information for agents to understand the payload format. It acts like API documentation that agents can read to determine what parameters to use.

Note that `payloadDescription` doesn't have to be in a certain format, as long as agents can understand it as natural language and generate the correct payload. Think of it as the comments and docs for your API, agents read it and decide what parameters to use. In practice, using JSON schema is recommended to match the format of training data.

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
toolkit.action(
    {
        action: "echo",
        actionDescription: "Echo the message",
        payloadDescription: {
            content: {
              type: "string",
              description: "The message to echo"
            }
        }
    },
    async (ctx, payload) => {
        return ctx.result(`You are agent <${ctx.agentId}>, you said "${payload?.content}".`);
    }
);
```
{% endtab %}

{% tab title="Python" %}
```
@toolkit.action(
    action="echo",
    action_description="Echo the message",
    payload_description={
        "content": {
            "type": "string",
            "description": "The message to echo"
        }
    },
)
async def echo(ctx: unifai.ActionContext, payload={}): # can be a sync function too
    return ctx.Result(f'You are agent <{ctx.agent_id}>, you said "{payload.get("content")}".')
```
{% endtab %}

{% tab title="Rust" %}
```
use thiserror::Error;
use unifai_sdk::{
    serde::{self, Deserialize, Serialize},
    serde_json::json,
    tokio,
    toolkit::*,
};

struct EchoChamber;

#[derive(Serialize, Deserialize)]
#[serde(crate = "serde")]
struct EchoChamberArgs {
    pub content: String,
}

#[derive(Debug, Error)]
#[error("Echo error")]
struct EchoChamberError;

impl Action for EchoChamber {
    const NAME: &'static str = "echo";

    type Error = EchoChamberError;
    type Args = EchoChamberArgs;
    type Output = String;

    async fn definition(&self) -> ActionDefinition {
        ActionDefinition {
            description: "Echo the message".to_string(),
            payload: json!({
                "content": {
                    "type": "string",
                    "description": "The message to echo"
                }
            }),
            payment: None,
        }
    }

    async fn call(
        &self,
        ctx: ActionContext,
        params: ActionParams<Self::Args>,
    ) -> Result<ActionResult<Self::Output>, Self::Error> {
        let output = format!(
            "You are agent <${}>, you said \"{}\".",
            ctx.agent_id, params.payload.content
        );

        Ok(ActionResult {
            payload: output,
            payment: None,
        })
    }
}

toolkit.add_action(EchoChamber);
```
{% endtab %}
{% endtabs %}

#### Start the Toolkit <a href="#start-the-toolkit" id="start-the-toolkit"></a>

Finally, start serving your toolkit:

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
await toolkit.run();
```
{% endtab %}

{% tab title="Python" %}
```
await toolkit.run()

# Or using asyncio.run():
# asyncio.run(toolkit.run())
```
{% endtab %}

{% tab title="Rust" %}
```
let runner = toolkit.start().await.unwrap();
let _ = runner.await.unwrap();
```
{% endtab %}
{% endtabs %}

Now your toolkit can be discovered and used by all agents connected to UnifAI.

#### Complete Example <a href="#complete-example" id="complete-example"></a>

Here's the complete code putting it all together:

{% tabs %}
{% tab title="JavaScript/TypeScript" %}
```
import { Toolkit } from 'unifai-sdk';

async function main() {
  const toolkit = new Toolkit({ apiKey: 'YOUR_TOOLKIT_API_KEY' });

  // Optionally update the toolkit details
  await toolkit.updateToolkit({ 
    name: "EchoChamber", 
    description: "What's in, what's out." 
  });

  // Register an action handler
  toolkit.action(
    {
      action: "echo",
      actionDescription: "Echo the message",
      payloadDescription: {
        content: { type: "string" }
      }
    },
    async (ctx, payload) => {
      return ctx.result(`You are agent <${ctx.agentId}>, you said "${payload?.content}".`);
    }
  );

  // Start serving the toolkit
  await toolkit.run();
}

main().catch(console.error);
```
{% endtab %}

{% tab title="Python" %}
```
import unifai
import asyncio

toolkit = unifai.Toolkit(api_key='YOUR_TOOLKIT_API_KEY')

# Update the toolkit details
asyncio.run(toolkit.update_toolkit(name="EchoChamber", description="What's in, what's out."))

# Register an action handler
@toolkit.action(
    action="echo",
    action_description="Echo the message",
    payload_description={"content": {"type": "string"}},
)
async def echo(ctx: unifai.ActionContext, payload={}):
    return ctx.Result(f'You are agent <{ctx.agent_id}>, you said "{payload.get("content")}".')

# Start serving the toolkit
asyncio.run(toolkit.run())
```
{% endtab %}

{% tab title="Rust" %}
```
use thiserror::Error;
use unifai_sdk::{
    serde::{self, Deserialize, Serialize},
    serde_json::json,
    tokio,
    toolkit::*,
};

struct EchoChamber;

#[derive(Serialize, Deserialize)]
#[serde(crate = "serde")]
struct EchoChamberArgs {
    pub content: String,
}

#[derive(Debug, Error)]
#[error("Echo error")]
struct EchoChamberError;

impl Action for EchoChamber {
    const NAME: &'static str = "echo";

    type Error = EchoChamberError;
    type Args = EchoChamberArgs;
    type Output = String;

    async fn definition(&self) -> ActionDefinition {
        ActionDefinition {
            description: "Echo the message".to_string(),
            payload: json!({
                "content": {
                    "type": "string",
                    "description": "The message to echo",
                    "required": true
                }
            }),
            payment: None,
        }
    }

    async fn call(
        &self,
        ctx: ActionContext,
        params: ActionParams<Self::Args>,
    ) -> Result<ActionResult<Self::Output>, Self::Error> {
        let output = format!(
            "You are agent <${}>, you said \"{}\".",
            ctx.agent_id, params.payload.content
        );

        Ok(ActionResult {
            payload: output,
            payment: None,
        })
    }
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().init();

    let mut toolkit = ToolkitService::new("YOUR_TOOLKIT_API_KEY");

    let info = ToolkitInfo {
        name: "EchoChamber".to_string(),
        description: "What's in, what's out.".to_string(),
    };

    toolkit.update_info(info).await.unwrap();

    toolkit.add_action(EchoChamber);

    let runner = toolkit.start().await.unwrap();
    let _ = runner.await.unwrap();
}
```
{% endtab %}
{% endtabs %}

### Toolkit Examples <a href="#toolkit-examples" id="toolkit-examples"></a>

We open source our official toolkits at [unifai-network/unifai-toolkits](https://github.com/unifai-network/unifai-toolkits).
