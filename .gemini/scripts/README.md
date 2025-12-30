# Gemini Scripts

This directory contains utility scripts to support the Gemini Agent's workflows and project development lifecycle.

## Scripts

### `prune_history.py`

A maintenance script designed to keep the project's task history and progress log clean and manageable. As the project evolves, completed tasks and old progress entries can clutter the workspace. This script archives them to `.gemini/archive/`.

#### Workflow Integration

This script is part of the **Project-Wide Development Workflow** (see `memory-bank/systemContext.md`). It should be run periodically (e.g., monthly or after major releases) to ensure the `tasks/` directory and `memory-bank/progress.md` remain focused on current and recent activities.

#### Usage

Run the script from the project root:

```bash
python3 .gemini/scripts/prune_history.py [OPTIONS]
```

#### Options

* `--days DAYS`: The age in days for items to be considered "old" and ready for archiving. Defaults to **60 days**.
* `--dry-run`: Perform a scan and print what *would* be archived without actually moving any files or modifying `progress.md`. **Recommended for first-time use.**

#### Behavior

1. **Task Archiving**:
    * Scans `tasks/completed/` for markdown files.
    * Checks the file modification time.
    * If older than `DAYS`, moves the file to `.gemini/archive/tasks/`.

2. **Progress Log Archiving**:
    * Parses `memory-bank/progress.md`.
    * Identifies "Recent Milestones" and "Completed Tasks" entries.
    * Extracts dates (e.g., `2025-12-29`) from the entries.
    * If the date is older than `DAYS`, removes the entry from `progress.md`.
    * Appends the removed entries to `.gemini/archive/progress_archive.md` with a timestamp header.

#### Example

Archive items older than 90 days:

```bash
python3 .gemini/scripts/prune_history.py --days 90
```

Check what would be archived (dry run):

```bash
python3 .gemini/scripts/prune_history.py --dry-run
```
