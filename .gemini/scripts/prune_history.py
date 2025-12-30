#!/usr/bin/env python3
import os
import shutil
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
TASKS_DIR = PROJECT_ROOT / "tasks"
COMPLETED_TASKS_DIR = TASKS_DIR / "completed"
MEMORY_BANK_DIR = PROJECT_ROOT / "memory-bank"
PROGRESS_FILE = MEMORY_BANK_DIR / "progress.md"
ARCHIVE_DIR = PROJECT_ROOT / ".gemini" / "archive"
TASKS_ARCHIVE_DIR = ARCHIVE_DIR / "tasks"
PROGRESS_ARCHIVE_FILE = ARCHIVE_DIR / "progress_archive.md"

# Regex for dates in progress.md
# Matches: - **2025-12-29**: ...
# Matches: - [x] ... (2025-12-29)
DATE_REGEX = re.compile(r"(\d{4}-\d{2}-\d{2})")

def setup_archive_dirs():
    if not ARCHIVE_DIR.exists():
        print(f"Creating archive directory: {ARCHIVE_DIR}")
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        
    if not TASKS_ARCHIVE_DIR.exists():
        TASKS_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        
    if not PROGRESS_ARCHIVE_FILE.exists():
        PROGRESS_ARCHIVE_FILE.touch()
        with open(PROGRESS_ARCHIVE_FILE, "w") as f:
            f.write("# Progress Archive\n\n")

def get_file_age_days(file_path):
    mtime = os.path.getmtime(file_path)
    dt_mtime = datetime.fromtimestamp(mtime)
    delta = datetime.now() - dt_mtime
    return delta.days

def prune_tasks(days, dry_run=False):
    print(f"Scanning {COMPLETED_TASKS_DIR} for tasks older than {days} days...")
    count = 0
    if not COMPLETED_TASKS_DIR.exists():
        print("No completed tasks directory found.")
        return

    for task_file in COMPLETED_TASKS_DIR.glob("*.md"):
        age = get_file_age_days(task_file)
        if age > days:
            count += 1
            dest = TASKS_ARCHIVE_DIR / task_file.name
            print(f"  [ARCHIVE] {task_file.name} (Age: {age} days)")
            if not dry_run:
                shutil.move(str(task_file), str(dest))
    
    if count == 0:
        print("  No tasks to archive.")
    else:
        print(f"  Archived {count} tasks.")

def prune_progress(days, dry_run=False):
    print(f"Scanning {PROGRESS_FILE} for entries older than {days} days...")
    if not PROGRESS_FILE.exists():
        print("No progress file found.")
        return

    cutoff_date = datetime.now() - timedelta(days=days)
    
    with open(PROGRESS_FILE, "r") as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []
    archived_milestones = []
    archived_tasks = []
    
    in_milestones = False
    in_completed_tasks = False
    skipping_milestone_block = False
    skipping_task_block = False
    
    for line in lines:
        if line.startswith("## "):
            in_milestones = False
            in_completed_tasks = False
            skipping_milestone_block = False
            skipping_task_block = False
            
            if "Recent Milestones" in line:
                in_milestones = True
            elif "Completed Tasks" in line:
                in_completed_tasks = True
            
            new_lines.append(line)
            continue

        # Check for top-level list item (starts with - or * and no indentation)
        is_top_level = line.startswith("-") or line.startswith("*")
        
        if in_milestones:
            if is_top_level:
                match = DATE_REGEX.search(line)
                should_prune = False
                if match:
                    try:
                        d = datetime.strptime(match.group(1), "%Y-%m-%d")
                        if d < cutoff_date:
                            should_prune = True
                    except ValueError:
                        pass # Ignore invalid dates
                
                if should_prune:
                    skipping_milestone_block = True
                    archived_milestones.append(line)
                else:
                    skipping_milestone_block = False
                    new_lines.append(line)
            elif skipping_milestone_block:
                archived_milestones.append(line)
            else:
                new_lines.append(line)
                
        elif in_completed_tasks:
             if is_top_level:
                match = DATE_REGEX.search(line)
                should_prune = False
                if match:
                    try:
                        d = datetime.strptime(match.group(1), "%Y-%m-%d")
                        if d < cutoff_date:
                            should_prune = True
                    except ValueError:
                        pass
                
                if should_prune:
                    skipping_task_block = True
                    archived_tasks.append(line)
                else:
                    skipping_task_block = False
                    new_lines.append(line)
             elif skipping_task_block:
                archived_tasks.append(line)
             else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    total_archived = len(archived_milestones) + len(archived_tasks)
    
    if total_archived > 0:
        print(f"  Found {len(archived_milestones)} milestone lines and {len(archived_tasks)} task lines to archive.")
        
        if not dry_run:
            # Write back to progress.md
            with open(PROGRESS_FILE, "w") as f:
                f.write("\n".join(new_lines) + "\n")
            
            # Append to archive
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(PROGRESS_ARCHIVE_FILE, "a") as f:
                f.write(f"\n## Archived on {timestamp}\n\n")
                if archived_milestones:
                    f.write("### Milestones\n")
                    f.write("\n".join(archived_milestones) + "\n\n")
                if archived_tasks:
                    f.write("### Completed Tasks\n")
                    f.write("\n".join(archived_tasks) + "\n\n")
            print("  Progress file updated and archive written.")
    else:
        print("  No progress entries to archive.")

def main():
    parser = argparse.ArgumentParser(description="Prune old tasks and progress entries.")
    parser.add_argument("--days", type=int, default=60, help="Age in days to archive (default: 60)")
    parser.add_argument("--dry-run", action="store_true", help="Scan without moving files")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN: No changes will be made.")
    else:
        print(f"PRUNING MODE: Archiving items older than {args.days} days.")
        
    setup_archive_dirs()
    prune_tasks(args.days, args.dry_run)
    prune_progress(args.days, args.dry_run)

if __name__ == "__main__":
    main()
