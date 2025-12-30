<div align="center">
  <img src="logo.jpg" alt="geminiFlow" width="350">
</div>

**geminiFlow** is a foundational setup for reliable, agentic [Gemini CLI](https://geminicli.com/) workflows. It provides a structured environment and pre-configured tools to jumpstart your AI-assisted development.

> [!TIP]
> **Start Here**: For deep operational details and the core workflow philosophy, please read [GEMINI.md](.gemini/GEMINI.md) first.

## 🚀 Getting Started

### Prerequisites

- **Node.js & NPM**: Required for the `context7` MCP server.
- **Python (uv recommended)**: Required for the `ast-grep` MCP server.

### Installation

1. Clone this repository.
2. Review the configuration files in `.gemini/`.
3. Configure your MCP servers as described below.

---

## ⚙️ Configuration & MCP Servers

The core configuration lives in [`.gemini/settings.json`](.gemini/settings.json). This file pre-configures two powerful Model Context Protocol (MCP) servers.

### 1. @upstash/context7-mcp

- **Status**: Automatic Installation

- **Action Required**: Add your API Key.
This server will automatically install via `npx` on systems with NPM available. You simply need to open `settings.json` and replace `KEY_HERE` with your actual API key.

### 2. ast-grep-mcp

- **Status**: Manual Installation Required

- **Action Required**: Install server & update path.
This server provides structural code search capabilities. You must install it manually on your machine.

1. Follow the installation instructions at: [https://github.com/ast-grep/ast-grep-mcp](https://github.com/ast-grep/ast-grep-mcp)
2. Locate where the server was installed (e.g., path to `main.py`).
3. Update specific path in [`.gemini/settings.json`](.gemini/settings.json) to point to your local installation.

---

## 📂 Directory Structure

The `.gemini/` directory is the brain of this workflow:

- **`GEMINI.md`**: The master system prompt and operational protocol.
- **`settings.json`**: Tool and server configurations.
- **`templates/`**: Standardized file templates for consistency.
- **`scripts/`**: Utility scripts for maintenance and automation.
