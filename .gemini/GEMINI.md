# SYSTEM: GEMINI || MODE: AGENT_CLI

## 0. BOOT_SEQUENCE

**VARS**: `$MB=./memory-bank`, `$TASKS=./tasks`

1. **INIT**:
   * **IF ABSENT** `$MB`: **MKDIR** `$MB` -> **CP** `.gemini/templates/*` `$MB/` -> **MV** `$MB/*.template.md` `$MB/*.md`.
   * **IF ABSENT** `$TASKS`: **MKDIR** `$TASKS`.
2. **LOAD_CTX**: **READ** `$MB/projectBrief.md` `$MB/progress.md` `$MB/systemContext.md` `$MB/activeContext.md`.
3. **RECON**:
   * **MAP**: Delegate to `codebase_investigator` (Architecture/Flows) or `glob` (Files).
   * **SEARCH**: **PREFER** `find_code` (Simple) > `find_code_by_rule` (Complex) > `search_file_content` (Text). **DEBUG**: `dump_syntax_tree` (Pattern) / `test_match_code_rule` (Rule).
   * **DOCS**: **VERIFY** libs via `resolve-library-id` -> `get-library-docs` (target `topic`).
4. **ALIGN**: IF `activeContext` ref `task_id` -> **READ** `$TASKS/<task_id>.md`.

## 1. TASK_PROTOCOL (State Machine)

**Structure**: `$MB/progress.md` (Epics) -> `$TASKS/*.md` (Stories) -> `$MB/activeContext.md` (State).
**Guard**: Large Tasks -> **REQUIRE** Detailed Plan (Docs/Patterns) + Multi-Session. **SIGNAL** Reset on Phase Done.

* **Task File** (`$TASKS/task_name.md`):
  * **Frontmatter**: `Title`, `Status` (OPEN|IN_PROGRESS|BLOCKED|DONE).
  * **Phases**:
    1. **DISCOVERY**: Context gathering. **Strategy**: AST (`find_code`|`find_code_by_rule`) > Text (`grep`). **Validation**: `dump_syntax_tree`/`test_match_code_rule` (AST) | `resolve-library-id` (Libs).
    2. **SPEC**: Requirements, Test Plan & Docs/Examples (`get-library-docs`).
    3. **IMPL**: Code generation (TDD).
    4. **VERIFY**: Test execution & Manual confirmation. (Stubborn Debug: `resolve-library-id` -> `get-library-docs`).
* **Transition**: Update `$TASKS` Checkbox [x] -> **MOVE** to `$TASKS/completed/` -> Update `$MB/progress.md` -> Update `$MB/activeContext.md`.

## 2. OPERATIONAL LOOP

### A. PLAN

1. **Check**: Current Phase of `activeTask`.
2. **Strategy**:
   * IF `AMBIGUOUS`: **STOP** -> **QUERY** User (Specific Qs).
   * IF `DISCOVERY`: **INVESTIGATE** -> **UPDATE** Task Context.
   * IF `SPEC`: **RESOLVE** Libs (`context7p`) -> **WRITE** Plan in Task File.
   * IF `IMPL`/`VERIFY`: **UPDATE** `activeContext.md` (Session focus) -> **ACT**.

### B. EXECUTE

1. **Work**: Perform action (Code, Test, or Refactor). **PREFER** AST-based search. **CONSTRAINT**: Placeholders allowed **ONLY** in SCAFFOLD.
2. **Env**: **DETECT** & **USE** isolated env (venv/poetry/node_modules/cargo). Prefer local bins > global.
3. **IO**: Minimize output (quiet flags, redir to temp).
4. **Verify**: Run lint/test. **NEVER** leave broken builds. (Stubborn Debug: `resolve-library-id` -> `get-library-docs`).

### C. PERSIST

**INVARIANT**: Chat is ephemeral. Files are eternal.

1. **Sync**: Update `$TASKS` & `$MB/activeContext.md`. Refine `$MB/systemContext.md` if arch changes.
2. **Output**: Return terse confirmation of State Change.
3. **Reset**: IF (Phase/Task DONE) -> **BACKFILL** (Learnings -> $TASKS/$MB) -> **PROMPT** Session End. **CONSTRAINT**: 1 Major Phase/Task per Session (Bias: Conservative).

## 3. INTERFACE

* **Voice**: Terse (Ops). Concise pre-tool explain. Code > Prose.
* **Safety**: Verify paths internally. Confirm context. Verify APIs.
