# System Context

## Architecture & Design Patterns

### Architecture Style

*   **[Style Name]:** [Description]
*   **[Component 1]:** [Description]
*   **[Component 2]:** [Description]

### Key Design Patterns

#### 1. [Pattern Name]

- **Intent**: [Description]
- **Structure**: [Description]
- **Integration**: [Description]

#### 2. [Pattern Name]

- **Intent**: [Description]
- **Structure**: [Description]
- **Integration**: [Description]

## Project-Wide Development Workflow

### Workspace Management
- **[Virtual Root/Environment]:** [Description]
- **[Tooling]:** [Description]

### Development Utilities

- **Prune History Script**: `.gemini/scripts/prune_history.py`
    - **Purpose**: Manage the growth of `tasks/completed/` and `memory-bank/progress.md` by archiving old entries.
    - **Usage**: `.gemini/scripts/prune_history.py [--days DAYS] [--dry-run]`
    - **Default**: Archives items older than 60 days to `.gemini/archive/`.

### Testing Strategy
- **[Strategy]:** [Description]

## Technical Context

### Stack & Modules

- **Language**: [Language & Version]
- **Dependency Manager**: [Tool]
- **Project Layout**: [Description]

### External Services

- **[Service 1]:** [Description]
- **[Service 2]:** [Description]

### Environment & Config

- **[Config Aspect]:** [Description]
