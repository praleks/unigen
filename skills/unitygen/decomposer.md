# Game Decomposer

Decompose a game into a development plan — a small number of large tasks, each independently verifiable. Output: `PLAN.md`.

## Workflow

1. Read `reference.png` — camera, complexity, entity count, environment scope.
2. Read the game description.
3. Identify algorithmic risks — procedural gen, custom shaders, novel physics, hard pathfinding. Only those merit isolation.
4. Bundle routine work into few large tasks.
5. Write `PLAN.md`.

**Minimize task count.** Typical 2D arcade: ≤3 tasks. Hard algorithms: up to ~7.

### What Counts as "Hard" (Isolate)

- Procedural meshes, runtime CSG, heavy mesh deformation
- Custom URP/HDRP shaders, complex post stacks
- Vehicle physics, rope, advanced IK blends
- Dynamic navmesh / crowd / flocking at scale
- Cinematic cameras with collision and blending

### What Counts as "Routine" (Bundle)

- `CharacterController` or Rigidbody movement, jumps, slopes
- Triggers, pickups, damage zones
- Animator-driven states, blend trees
- Tilemaps / grid layouts / modular level pieces
- UI Canvas, HUD, pause
- Spawning, timers, waves
- Simple follow cameras, Cinemachine basic setup

## Output Format

Produce `PLAN.md`:

````markdown
# Game Plan: {Game Name}

## Game Description

{Verbatim user description.}

## 1. {Task Name}
- **Depends on:** (none)
- **Goal:** ...
- **Requirements:**
  - ...
- **Assets needed:** ...
- **Verify:** ...

## 2. {Task Name}
- **Depends on:** 1
- ...
````

### Task Fields

- **Depends on** — prior task numbers or `(none)`.
- **Goal** — player-visible outcomes, not implementation recipes.
- **Requirements** — testable behavior; concrete feel only when it matters.
- **Assets needed** — types and roles; asset planner fills files and **Assets:** assignments.
- **Verify** — what screenshots or short capture must show.

## Mandatory Final Task: Presentation

Last task is a showcase deliverable:

```markdown
## N. Presentation
- **Depends on:** {all other tasks}
- **Goal:** Short gameplay showcase suitable for sharing.
- **Requirements:**
  - Prefer Unity Recorder (if package present) to export MP4, OR a documented sequence of high-quality Play Mode screenshots + short screen recording note
  - ~20–40s of representative motion if video
  - Output under `screenshots/presentation/` (e.g. `gameplay.mp4` or `shot_01.png` …)
  - 3D: clear lighting, readable motion; 2D: camera motion or scroll that shows core loop
- **Verify:** Smooth video without glitches OR a numbered set of screenshots covering the core loop with no obvious defects.
```

Adapt 2D/3D bullets to the game.

## What NOT to Include

- C# snippets or MCP call dumps
- Micro-tasks for routine UI or collisions
- Non-visual verification only
