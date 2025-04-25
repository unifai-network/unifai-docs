---
sidebar_position: 8
title: Frequently Asked Questions
---

# Frequently Asked Questions

## Getting Started

### How do I get my API keys?
- Visit [UnifAI](https://app.unifai.network/) to register and obtain your Agent API key (for tools) and Toolkit API key (for creating toolkits).

### Where can I find code examples?
- Examples for both JavaScript/TypeScript and Python can be found within this documentation as well as in the SDK repositories. We also open source our official toolkits at [unifai-network/unifai-toolkits](https://github.com/unifai-network/unifai-toolkits).

## Technical Questions

### Can I use UnifAI with any LLM?
- Yes, UnifAI works with any LLM that supports function calling (OpenAI API compatible). For LLMs that aren't OpenAI compatible, you can use services like [OpenRouter](https://openrouter.ai/docs) to access them through an OpenAI-compatible API.

### Do I need both API keys?
- No, you only need the API key for your use case:
  - Use the Agent API key if you're building applications that use tools
  - Use the Toolkit API key if you're creating and serving tools

### How does tool discovery work?
- Tools are discovered dynamically at runtime based on the agent's needs. The agent can search for tools using keywords and descriptions, and UnifAI will return relevant tools that match the requirements.

## Contributing

### How do I contribute?
- Contributions are welcome! Please submit a Pull Request or open an issue on our repository with your suggestions and improvements.

### Can I publish my own tools?
- Yes, you can create and publish your own toolkits to the UnifAI marketplace. See the [Creating Toolkits](/creating-toolkits) section for details.

### Where can I get help?
- Check our [GitHub repositories](https://github.com/unifai-network/) for issues and discussions
- Review the documentation for detailed guides and examples
