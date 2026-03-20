Use `/unitygen` to generate or update this game from a natural language description.

Visual quality is the top priority. Example failures:
- Generating a detailed image then shrinking it to a tile — details become tiny and clunky. Generate with shapes appropriate for the target size.
- Tiling textures where a single high-quality drawn background is needed
- Using sprite sheets for fire, smoke, or water instead of particles or shaders

# Session Instructions

Non-interactive background process spawned by Teleforge. No terminal, no stdin, no interactive UI. User is on Telegram — reach them **only** via MCP tools.

## unitygen orchestrator

1. `check_messages` before starting each new task and before ending the session.
2. After creating PLAN.md: `send_image` `reference.png` with the plan summary.
3. After each task: `send_image` best screenshot, task summary and visual QA verdict (pass/fail, key issues, rebuilds triggered). Never skip the verdict even on pass.
4. After all tasks: `send_video` final video if under 50MB, else `send_image` the best presentation stills.

## unity-task

Acts as a pulse — `send_message` a one-liner whenever it changes approach so the user never sees a long silent run.

# Project Structure

Unity game root once `/unitygen` runs:

```
Assets/
  Scenes/           # .unity scenes
  Scripts/          # C# gameplay
  Prefabs/
  (Materials, Models, Textures, …)
ProjectSettings/
Packages/
reference.png       # Visual target
STRUCTURE.md        # Architecture
PLAN.md             # Task DAG
ASSETS.md           # Asset manifest + art direction
MEMORY.md           # Task notes
assets/             # often gitignored — img/*.png, glb/*.gb from pipeline
screenshots/        # gitignored — captures per task
visual-qa/*.md      # OpenRouter vision QA reports
```

Working directory is the project root. Avoid unnecessary `cd` — use relative paths.

## Limitations

- No audio pipeline in skills
- Animated GLBs — static Tripo3D meshes only unless you extend tooling
