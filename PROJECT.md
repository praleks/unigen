# Unitygen — AI game pipeline (Unity + MCP + OpenRouter)

## What this is

**Unitygen** turns a short design sentence into a working **Unity** project: staged planning, reference imagery, optional Tripo3D meshes, C# and scenes driven through the **Unity Editor via MCP**, screenshots from Play Mode or the editor, and **vision QA** through **OpenRouter** multimodal models.

It is implemented as two skills: **unitygen** (orchestrator) and **unity-task** (one task per forked run). Stages load from small markdown files only when needed so context stays focused.

## Why visual verification

Text-only review misses z-fighting, wrong scale, broken materials, and animation pops. The executor captures frames and runs `visual_qa.py`, which sends reference + captures to a vision model through OpenRouter. Failures feed back into fixes or orchestrator replanning.

## Pipeline (summary)

1. **Visual target** — `asset_gen.py image` (OpenRouter image modalities) → `reference.png`, seed `ASSETS.md`.
2. **Decompose** — `PLAN.md`: few large tasks; only genuinely risky systems isolated.
3. **Scaffold** — `STRUCTURE.md`, `Assets/` layout, C# stubs, scenes via MCP; `read_console` until compile-clean.
4. **Assets** — planner fills `ASSETS.md`, runs CLI tools, assigns paths in `PLAN.md`.
5. **Tasks** — orchestrator dispatches **unity-task**: MCP for hierarchy/scripts, play and screenshot, VQA script, `MEMORY.md` updates.
6. **Presentation** — final task: Unity Recorder MP4 when available, else a defined screenshot set.

## OpenRouter and tools

- **Images:** `skills/unitygen/tools/asset_gen.py` → `/api/v1/chat/completions` with `modalities` and `image_config` per [OpenRouter image generation](https://openrouter.ai/docs/guides/overview/multimodal/image-generation).
- **Vision QA:** `skills/unity-task/scripts/visual_qa.py` → same API with image inputs per [image inputs](https://openrouter.ai/docs/guides/overview/multimodal/images).
- **Tripo3D:** unchanged HTTP client in `tripo3d.py`.

## Publishing

`publish.sh` copies `skills/` to `<target>/.claude/skills/` and installs `CLAUDE.md` (default `teleforge.md`). The Unity project itself is the working tree — skills only instruct the agent.

## Compared to the prior Godot stack

The old pipeline used headless Godot, GDScript scene builders, and a bundled 850-file API doc. Unitygen trades that for **live Editor MCP**, **C#**, and **public Unity documentation** linked from skill files — no vendored class encyclopedia.

## Output

A Unity project under version control (excluding `Library/`, `Temp/`, etc.), plus markdown artifacts (`PLAN.md`, `STRUCTURE.md`, `ASSETS.md`, `MEMORY.md`, `visual-qa/`) that coordinate humans and agents.
