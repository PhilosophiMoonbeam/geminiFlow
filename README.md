<div align="center">
  <img src="logo.jpg" alt="geminiFlow" width="350">
</div>

**geminiMind** is a foundational setup for reliable, agentic [Gemini CLI](https://geminicli.com/) workflows. It provides a structured environment and pre-configured tools to jumpstart your AI-assisted development.

> [!TIP]
> **Start Here**: For deep operational details and the core workflow philosophy, please read [GEMINI.md](.gemini/GEMINI.md) first.

---

## 💠 Workflow Diagram

### 1. Data Structure & Boot Sequence
This diagram focuses on the file system hierarchy, persistent variables (`$MB`, `$TASKS`), and the initialization logic (Step 0).

```mermaid
flowchart TD
    %% Styling
    classDef file fill:#f0fdf4,stroke:#22c55e,stroke-width:2px,color:#000,stroke-dasharray: 5 5
    classDef process fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#000
    classDef decision fill:#fefce8,stroke:#eab308,stroke-width:2px,color:#000

    %% --- STORAGE HIERARCHY ---
    subgraph Storage ["💾 File System / Variables"]
        direction TB
        Tpl[/"📂 .gemini/templates/*"\]:::file
        MB[("🧠 $MB (Memory Bank)\n- projectBrief.md\n- progress.md\n- systemContext.md")]:::file
        Ctx[("📄 $CTX\n(activeContext.md)")]:::file
        Tasks[("📋 $TASKS\n- <task_id>.md")]:::file
    end

    %% --- BOOT SEQUENCE ---
    subgraph Boot ["🚀 0. BOOT_SEQUENCE"]
        direction TB
        Start((Boot))
        Init{Check $MB?}:::decision
        Mkdir(Mkdir & Copy Tpl):::process
        Load(READ $MB + $CTX):::process
        Align{Ctx refs Task?}:::decision
        ReadTask(READ $TASKS/<id>):::process
        Ready([Ready for Loop]):::process

        Start --> Init
        Init -->|No| Mkdir
        Mkdir -->|Populate| MB
        Init -->|Yes| Load
        Mkdir --> Load
        
        Load --> Align
        Align -->|Yes| ReadTask
        Align -->|No| Ready
        ReadTask --> Ready
    end

    %% Data Relationships
    Tpl -.-> Mkdir
    MB -.-> Load
    Ctx -.-> Load
    Tasks -.-> ReadTask
```

---

### 2. The Operational Loop (High Level)
This diagram abstracts away the specific coding tools to focus on the Agent's decision-making "heartbeat" (Step 2). It determines *what* to do next.

```mermaid
flowchart TD
    %% Styling
    classDef process fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#000
    classDef decision fill:#fefce8,stroke:#eab308,stroke-width:2px,color:#000
    classDef stop fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
    classDef subSystem fill:#f3e8ff,stroke:#a855f7,stroke-width:2px,color:#000

    Start((Start Tick)) --> Sync
    
    subgraph Loop ["⚙️ 2. OPERATIONAL LOOP"]
        Sync(1. SYNC: Read $CTX):::process
        Strategy{2. STRATEGY}:::decision
        
        %% Outcomes
        Stop([STOP: Ambiguous/Ask User]):::stop
        FixCtx(Update $CTX Phase):::process
        RunProtocol[[EXECUTE: Run Task Protocol]]:::subSystem
        Persist(3. PERSIST: Save State):::process

        %% Flow
        Sync --> Strategy
        Strategy -->|Ambiguous| Stop
        Strategy -->|Phase Mismatch| FixCtx
        FixCtx --> Sync
        Strategy -->|Execute| RunProtocol
        
        RunProtocol --> Persist
        Persist -->|Next Tick| Sync
    end
```

---

### 3. The Task Protocol (Detailed Execution)
This diagram details the "State Machine" inside the Execution phase (Step 1). It includes the specific tools (`glob`, `find_code`, `query-docs`) and the **Completion Logic**.

```mermaid
flowchart TD
    %% Styling
    classDef phase fill:#f3e8ff,stroke:#a855f7,stroke-width:2px,color:#000
    classDef tool fill:#e0f2fe,stroke:#0ea5e9,stroke-width:1px,color:#000
    classDef decision fill:#fefce8,stroke:#eab308,stroke-width:2px,color:#000
    classDef action fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#000

    Input((Execute)) --> CheckPhase{Check Phase}

    subgraph Protocol ["1. TASK_PROTOCOL"]
        
        %% PHASE 1
        subgraph P1 [Discovery]
            direction TB
            DNode(DISCOVERY):::phase
            DTools["🛠 map / glob\n🛠 find_code\n🛠 resolve-library-id"]:::tool
            DNode --- DTools
        end

        %% PHASE 2
        subgraph P2 [Spec]
            direction TB
            SNode(SPEC):::phase
            STools["🛠 query-docs (Patterns)"]:::tool
            Plan(📝 Write Plan to $TASKS):::action
            SNode --- STools
            STools --> Plan
        end

        %% PHASE 3
        subgraph P3 [Impl]
            direction TB
            INode(IMPL):::phase
            ITools["🛠 find_code -> replace\n🛠 write"]:::tool
            LoopTDD(🔁 TDD Loop):::process
            INode --- ITools
            ITools --- LoopTDD
        end

        %% PHASE 4
        subgraph P4 [Verify]
            direction TB
            VNode(VERIFY):::phase
            RunTest{Pass Tests?}:::decision
            Debug("🛠 Debug: query-docs\n(Check Assumptions)"):::tool
            VNode --> RunTest
            RunTest -->|No| Debug
            Debug -.->|Fix| INode
        end

        %% TRANSITIONS
        CheckPhase -->|Discovery| DNode
        CheckPhase -->|Spec| SNode
        CheckPhase -->|Impl| INode
        CheckPhase -->|Verify| VNode

        DNode --> SNode
        Plan --> INode
        INode --> VNode
    end

    %% COMPLETION LOGIC
    subgraph DoneLogic ["🏁 TRANSITION: DONE"]
        IsDone{Task Complete?}:::decision
        MoveFile[📂 MV to $TASKS/completed/ \n 🧹 CLEAR $CTX task_id]:::action
        UpdateMB[📝 Update $MB/progress.md]:::action
    end

    RunTest -->|Yes| IsDone
    IsDone -->|No| Exit((Persist))
    IsDone -->|Yes| MoveFile
    MoveFile --> UpdateMB
    UpdateMB --> Exit
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
