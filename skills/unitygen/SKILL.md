---
name: unitygen
description: |
  This skill should be used when the user asks to "make a game", "build a game", "generate a game", or wants to generate or update a complete Unity game from a natural language description.
---

# Game Generator — Orchestrator

Generate and update Unity games from natural language.

## Capabilities

Read each sub-file from `${CLAUDE_SKILL_DIR}/` when you reach its pipeline stage.

| File | Purpose |
|------|---------|
| `visual-target.md` | Reference image for art direction |
| `decomposer.md` | Decompose into `PLAN.md` |
| `scaffold.md` | Architecture and Unity project skeleton |
| `asset-planner.md` | Asset list within budget |
| `asset-gen.md` | PNGs (OpenRouter) and GLBs (Tripo3D) |

## Pipeline

```
User request
    |
    +- Resume if PLAN.md exists -> read PLAN.md, STRUCTURE.md, MEMORY.md -> task execution
    |
    +- Visual target -> reference.png + ASSETS.md
    +- Decompose -> PLAN.md
    +- Scaffold -> STRUCTURE.md + Unity layout + C# stubs
    |
    +- If budget and no filled ASSETS.md tables:
    |   +- Plan and generate assets -> ASSETS.md + PLAN.md asset assignments
    |
    +- For each task in PLAN.md:
    |   +- Set **Status:** pending, fill **Targets:** (Assets/ paths)
    |
    +- Summarize plan for user
    |
    +- While ready task exists:
    |   +- PLAN.md: in_progress
    |   +- Skill(skill="unity-task") with full task block
    |   +- done or replan; git commit
    |
    +- Summary
```

Task **Status:** `pending` | `in_progress` | `done` | `done (partial)` | `skipped`.

## Running Tasks

```
Skill(skill="unity-task") with argument:
  ## N. {Task Name}
  - **Status:** in_progress
  - **Targets:** Assets/Scenes/Main.unity, Assets/Scripts/PlayerController.cs
  - **Goal:** ...
  - **Requirements:** ...
  - **Verify:** ...
```

If `Skill` is unavailable, spawn a sub-agent with the same block.

## Visual QA

Runs inside unity-task. **Never ignore fail** — act before marking done, or replan / escalate per failure notes in unity-task.

## Debugging

Read `MEMORY.md`, `screenshots/`, Unity `read_console` via MCP for compile errors.
