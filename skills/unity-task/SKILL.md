---
name: unity-task
description: |
  Execute a single Unity development task — scenes, prefabs, C# scripts, verify visually via Unity MCP.
context: fork
---

# Unity Task Executor

All files below are in `${CLAUDE_SKILL_DIR}/`. Load progressively — read each file when its phase begins, not upfront.

| File | Purpose | When to read |
|------|---------|--------------|
| `quirks-unity.md` | Unity editor and C# pitfalls | Before writing any code |
| `csharp-patterns.md` | Minimal C# / Unity API conventions | Before writing C# |
| `capture.md` | Screenshots via Unity MCP | Before capturing |
| `visual-qa.md` | Automated VQA CLI | Task has visual output and `reference.png` exists |

MCP: use the Unity MCP server connected to the Editor. If multiple Unity instances are connected, call `set_active_instance` first. Before relying on new or edited scripts, call `read_console` and fix compile errors.

Execute a single development task from PLAN.md:

$ARGUMENTS

## Workflow

1. **Analyze the task** — read **Targets** (`Assets/...`, `.unity`, `.cs`, prefabs). Plan scene vs script order: hierarchy and components before runtime logic when both change.
2. **Unity MCP** — create or load scenes (`manage_scene`), create or modify GameObjects (`manage_gameobject`, `manage_components`, `manage_prefabs`), scripts (`create_script`, `manage_script`, `script_apply_edits`). Use paged `get_hierarchy` with modest `page_size` for large scenes; follow `next_cursor` until done.
3. **Compile loop** — after script changes, `read_console` (and `validate_script` if useful). Fix errors until clean.
4. **Play mode** — use `manage_editor` to enter/exit Play Mode when the task needs runtime verification. Re-check console after play.
5. **Screenshots** — `manage_scene` action `screenshot` (or project-specific capture path in `capture.md`). Store under `screenshots/{task_folder}/`.
6. **Manual visual check** — compare to **Verify** and to `reference.png` when present.
7. **Visual QA** — when applicable, run `visual_qa.py` per `visual-qa.md`.
8. **Report** — paths to screenshots, VQA report path or `skipped`, failures per Reporting section below.

## Iteration

Steps 2–7 form an implement → capture → verify loop. Stop if you repeat the same fix without convergence; report to the orchestrator.

## Reporting to Orchestrator

End with:
- **Screenshot path:** `screenshots/{task_folder}/` and which frames best show the result
- **What each screenshot shows** — one line per frame
- **VQA report:** `visual-qa/{N}.md` or `skipped`

On failure: what is wrong, what you tried, best guess at root cause.

## Project Memory

Read `MEMORY.md` before work; append useful discoveries after.

If the host has no `Skill` tool, run this executor in a fresh sub-agent session with the same task block.
