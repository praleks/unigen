# Unitygen: skills that build Unity projects with MCP + OpenRouter

[![Watch the video](https://img.youtube.com/vi/eUz19GROIpY/maxresdefault.jpg)](https://youtu.be/eUz19GROIpY)

[Watch the demos](https://youtu.be/eUz19GROIpY) · [Prompts](demo_prompts.md)

Describe the game you want. A staged pipeline plans architecture, generates art, implements C# and scenes through the **Unity Editor (MCP)**, captures screenshots, and runs **vision QA** via **OpenRouter**. Output is a real Unity project under `Assets/`.

## How it works

- **Two skills** — **unitygen** (orchestrator) and **unity-task** (per-task executor, forked context in Claude Code).
- **Unity MCP** — scenes, GameObjects, scripts, console, screenshots against a live Editor.
- **OpenRouter** — image generation and vision QA (`OPENROUTER_API_KEY`, optional `OPENROUTER_IMAGE_MODEL` / `OPENROUTER_VISION_MODEL`).
- **Tripo3D** — optional image-to-GLB for 3D (`TRIPO3D_API_KEY`).
- **Python tools** in `skills/unitygen/tools/` (`asset_gen.py`, rembg, sprite pipeline).

## Prerequisites

- **Unity** project + **Unity MCP** connected to the agent session (e.g. Cursor).
- **Python 3** + `pip install -r skills/unitygen/tools/requirements.txt`
- **API keys:** `OPENROUTER_API_KEY`; `TRIPO3D_API_KEY` for 3D mesh generation.
- **Claude Code** (or another client that supports skills / sub-agents) for published game folders.

## Create a game project

This repo is the skill source. Publish into a Unity project directory:

```bash
./publish.sh ~/my-unity-game          # uses teleforge.md as CLAUDE.md
./publish.sh ~/my-unity-game local.md
```

Open the target in your agent IDE, enable Unity MCP, run **`/unitygen`**, and describe the game.

## Notes

- Budget and asset CLI behavior match the previous generator; ledger entries use `openrouter_image` for image calls.
- Long runs suit a VM; GPU helps Unity Play Mode and captures, not the LLM.
- Default `teleforge.md` targets [Teleforge](https://github.com/htdt/teleforge) + Telegram MCP — swap `CLAUDE.md` if unused.

Follow progress: [@alex_erm](https://x.com/alex_erm)
