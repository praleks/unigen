We develop agents and skills here. They are used in another folder for Unity game development with an AI coding agent and **Unity MCP**.

## Layout

- `skills/` — skill definitions (`SKILL.md`) and tool scripts
- `teleforge.md` — default `CLAUDE.md` for published game folders (Telegram bridge)
- `publish.sh` — copy skills into a target project

## Skills

- **unitygen** — orchestrator: visual target, decompose, scaffold, asset plan, asset generation, task loop
- **unity-task** — single-task execution: Unity MCP, C#, capture, VQA (`context: fork`)

When writing skills: avoid obvious hand-holding — the model is capable; keep context lean.
