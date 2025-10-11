# 📚 Agent Documentation

### Introduction <a href="#introduction" id="introduction"></a>

We also provide developers with a powerful and flexible framework for building intelligent agents that can interact with users across multiple communication channels. This document provides comprehensive guidance on how to utilize the Agent functionality to create custom AI assistants tailored to your specific needs.

### Table of Contents <a href="#table-of-contents" id="table-of-contents"></a>

1. [Getting Started](https://docs.unifai.network/agent#getting-started)
2. [Agent Overview](https://docs.unifai.network/agent#agent-overview)
3. [Agent Configuration](https://docs.unifai.network/agent#agent-configuration)
   * [Initialization](https://docs.unifai.network/agent#initialization)
   * [Prompts Management](https://docs.unifai.network/agent#prompts-management)
   * [Model Configuration](https://docs.unifai.network/agent#model-configuration)
4. [Client Implementation](https://docs.unifai.network/agent#client-implementation)
   * [Available Clients](https://docs.unifai.network/agent#available-clients)
   * [Creating Custom Clients](https://docs.unifai.network/agent#creating-custom-clients)

### Getting Started <a href="#getting-started" id="getting-started"></a>

#### Installation <a href="#installation" id="installation"></a>

```
pip install unifai-sdk
```

#### Basic Usage <a href="#basic-usage" id="basic-usage"></a>

```
from unifai.agent import Agent
from unifai.client import TelegramClient
 
agent = Agent(api_key="YOUR_UNIFAI_AGENT_API_KEY")

telegram_client = TelegramClient(bot_token="YOUR_TELEGRAM_BOT_TOKEN")
agent.add_client(telegram_client)

agent.run()
```

### Agent Overview <a href="#agent-overview" id="agent-overview"></a>

The `Agent` class is the central component of the UnifAI SDK. It coordinates:

* Communication with users through various clients (Telegram, Twitter, Discord, etc.)
* Natural language processing using AI models
* Tools execution for performing actions

Agents are designed to be extensible, allowing developers to customize their behavior through prompts, model selection, etc.

### Agent Configuration <a href="#agent-configuration" id="agent-configuration"></a>

#### Initialization <a href="#initialization" id="initialization"></a>

The `Agent` class accepts several parameters during initialization to customize its behavior:

```
from unifai.agent import Agent

agent = Agent(
    api_key="YOUR_UNIFAI_API_KEY",
    agent_id="",  # Optional: Unique identifier for the agent, useful when running multiple agents that share the same database
    clients=[],  # Optional: List of client instances
    tool_call_concurrency=10,  # Optional: Number of concurrent tool calls
)
```

#### Prompts Management <a href="#prompts-management" id="prompts-management"></a>

```
# Get all prompts
all_prompts = agent.get_all_prompts()

# Get a specific prompt
system_prompt = agent.get_prompt("system")

# Set a custom prompt
agent.set_prompt("system", "You are a helpful AI assistant specialized in financial advice.")
```

#### Model Configuration <a href="#model-configuration" id="model-configuration"></a>

You can specify which AI models to use for different prompts:

```
# Get the model for a specific prompt
model = agent.get_model("default")  # Returns the model for the default prompt

# Set the default model
agent.set_model("default", "anthropic/claude-3-7-sonnet-20250219")
```

### Client Implementation <a href="#client-implementation" id="client-implementation"></a>

The UnifAI SDK supports multiple communication channels through its client architecture. Clients handle the specifics of each platform while presenting a consistent interface to the agent.

#### Available Clients <a href="#available-clients" id="available-clients"></a>

The SDK includes several built-in clients:

* **TelegramClient**: For interacting with users via Telegram
* **TwitterClient**: For interacting with users via Twitter
* **DiscordClient**: For interacting with users via Discord

#### Creating Custom Clients <a href="#creating-custom-clients" id="creating-custom-clients"></a>

You can create your own clients for platforms not natively supported by implementing the `BaseClient` interface:

```
from unifai.client.base import BaseClient, MessageContext, Message

class SlackClient(BaseClient):
    """Client implementation for Slack."""
    
    @property
    def client_id(self) -> str:
        """Get client ID"""

    async def start(self):
        """Start the client"""

    async def stop(self):
        """Stop the client"""

    async def receive_message(self) -> Optional[MessageContext]:
        """Receive a message from the client"""

    async def send_message(self, ctx: MessageContext, reply_messages: List[Message]):
        """Send a message"""
```
