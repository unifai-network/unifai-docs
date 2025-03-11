---
sidebar_position: 2
title: Getting Started
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Getting Started with UnifAI Network

This guide will help you set up your environment and get started with UnifAI's SDKs.

## Prerequisites

- Node.js (for JavaScript/TypeScript) or Python installed
- An account at [UnifAI](https://app.unifai.network/) to obtain your API keys

## Installation

<Tabs>
  <TabItem value="js" label="JavaScript/TypeScript">

```bash
npm install unifai-sdk
```

  </TabItem>
  <TabItem value="py" label="Python">

```bash
pip install unifai-sdk
```

  </TabItem>
  <TabItem value="rs" label="Rust">

```bash
cargo add unifai-sdk
```

  </TabItem>
</Tabs>

## API Keys

There are two types of API keys:
- **Agent API Key:** Use this key when integrating tools into your agents.
- **Toolkit API Key:** Use this key when creating and serving toolkits.

You only need to get the one you need.
