# Unity Capture

Screenshots live under `screenshots/` (typically gitignored). One subfolder per task (e.g. `task_01_core`).

## Editor screenshot

With Unity MCP `manage_scene`:

- `action`: `screenshot`
- Set `path` relative to `Assets/` or as required by the tool descriptor
- Optional `screenshot_super_size` for higher resolution

Save outputs into `screenshots/{task_folder}/` with clear names (`main_view.png`, `frame_01.png`, …).

## Play Mode sequences

1. Load the correct scene.
2. Enter Play Mode via `manage_editor` (per tool schema).
3. Run long enough to satisfy **Verify** (input simulation or timed wait as the task requires).
4. Capture one or more screenshots during or after play.
5. Exit Play Mode.
6. Check `read_console` for errors.

## Video (presentation task)

Prefer Unity Recorder package if already in the project, or record externally. If Recorder is unavailable, deliver a documented set of key screenshots plus orchestrator decision from `PLAN.md` final task.
