<div align="center">
  <img src="logo.jpg" alt="geminiFlow" width="350">
</div>

**geminiFlow** is a foundational setup for reliable, agentic [Gemini CLI](https://geminicli.com/) workflows. It provides a structured environment and pre-configured tools to jumpstart your AI-assisted development.

> [!TIP]
> **Start Here**: For deep operational details and the core workflow philosophy, please read [GEMINI.md](.gemini/GEMINI.md) first.

---

## 💠 Workflow Diagram

```mermaid
flowchart TD
    %% Styling
    classDef process fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#000
    classDef decision fill:#fefce8,stroke:#eab308,stroke-width:2px,color:#000
    classDef artifact fill:#f0fdf4,stroke:#22c55e,stroke-width:2px,color:#000,stroke-dasharray: 5 5
    classDef config fill:#f3e8ff,stroke:#a855f7,stroke-width:2px,color:#000
    classDef script fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000

    %% Nodes
    subgraph Boot_Sequence ["🚀 Boot Sequence"]
        direction TB
        Templates[/"📂 .gemini/templates/*"\]:::artifact
        Init(1. INIT: Project Setup):::process
        LoadCtx(2. LOAD_CTX: Read Context):::process
        Recon(3. RECON: Map & Search):::process
        
        Templates --> Init
        Init -->|Populate $MB| LoadCtx
        LoadCtx --> Recon
    end

    subgraph Operation ["⚙️ Operational Loop & Tools"]
        direction TB
        Settings[("⚙️ settings.json\n(MCP Config)")]:::config
        Plan(4. ALIGN / PLAN):::process
        Exec(5. EXECUTE: Code & Test):::process
        Persist(6. PERSIST: Sync & Reset):::process
        
        %% Tool Connections
        Settings -.->|Configures| AstGrep["AST Search (ast-grep)"]:::process
        Settings -.->|Configures| Context7["Docs/Libs (context7)"]:::process
        
        Recon --> Plan
        Plan --> AstGrep
        Plan --> Context7
        AstGrep --> Exec
        Context7 --> Exec
        Exec --> Persist
    end

    subgraph Artifacts ["💾 Memory Bank & State"]
        MB[("🧠 $MB (Memory Bank)\n- projectBrief.md\n- systemContext.md\n- progress.md")]:::artifact
        Tasks[("📋 $TASKS\n- Active Task Files\n- Completed")]:::artifact
    end

    subgraph Maintenance ["🧹 Maintenance"]
        PruneScript[["🐍 prune_history.py\n(Archive Old Tasks)"]]:::script
    end

    %% Data Flow
    Init -.-> MB
    Recon -.->|Read| MB
    Plan -.->|Read/Update| Tasks
    Persist -.->|Update| MB
    Persist -.->|Update| Tasks
    
    %% Maintenance Flow
    Tasks -.->|Periodic Pruning| PruneScript
    MB -.->|Periodic Pruning| PruneScript
    PruneScript -->|Moves to| Archive[/"📦 .gemini/archive"\]:::artifact

    %% Classes
    class Init,LoadCtx,Recon,Plan,Exec,Persist,AstGrep,Context7 process
    class Templates,MB,Tasks,Archive artifact
    class Settings config
    class PruneScript script
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js & NPM**: Required for the `context7` MCP server.
- **Python (uv recommended)**: Required for the `ast-grep` MCP server.

### Installation

1. Clone this repository.
2. Review the configuration files in `.gemini/`.
3. Configure your MCP servers as described below.

---

## 🧑‍💻 Common Prompts

```bash
INIT $MB -- PROJECT: Social Network for Rabbits
```

```bash
LOAD_FULL $MB -- THEN_CREATE $TASKS: Example Feature Request
```

```bash
LOAD_FULL $MB -- THEN_EXECUTE $TASKS
```

---

## ⚙️ Configuration & MCP Servers

The core configuration lives in [`.gemini/settings.json`](.gemini/settings.json). This file pre-configures two powerful Model Context Protocol (MCP) servers.

### 1. [@upstash/context7-mcp](https://github.com/upstash/context7)

Up-to-date lib/dependency documentation for Agents.

- **Status**: Automatic Installation

- **Action Required**: Add your API Key.
This server will automatically install via `npx` on systems with NPM available. You simply need to open `settings.json` and replace `KEY_HERE` with your actual API key.

### 2. [ast-grep-mcp](https://github.com/ast-grep/ast-grep-mcp)

Focused structural code search for Agents.

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
