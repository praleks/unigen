# Asset Planner

Decide assets, generate within budget. Read `${CLAUDE_SKILL_DIR}/asset-gen.md` for CLI.

## Input

- `budget_cents` from user (or iteration budget)
- `PLAN.md` Game Description and per-task **Assets needed**
- `STRUCTURE.md` **Asset Hints**
- `reference.png`

## Workflow

1. Cross-reference hints, plan, and reference for models, textures, backgrounds, sprites.
2. Prioritize by visual impact; reserve ~10% for retries.
3. Use **Art direction** from `ASSETS.md` contextually per asset type (not a blind prefix).
4. Generate images (parallel), review, one retry each if bad; convert approved refs to GLB in parallel.
5. Write `ASSETS.md` with **Size** column for every row (world units, tile repeat, pixel display size, sprite frame size).
6. Update `PLAN.md`: add **Assets:** with concrete paths under `assets/` for each task.

Costs match `asset-gen.md` table (OpenRouter image charges are approximate budget entries).

## Common Mistakes

Same as before: over-detailed tiles, wrong asset type for background, sprite sheet rules, one sheet per character, solid BG + rembg for transparency, Tripo3D needs clean studio reference (no rembg on white-bg ref).

## ASSETS.md table format

Use tables: 3D Models, Textures, Backgrounds, Sprites — columns Name, Description, Size, Image, GLB as applicable.

## PLAN.md assignments

````markdown
- **Assets:**
  - `car` GLB (`assets/glb/car.glb`) — scale to 4m
  - `grass` texture (`assets/img/grass.png`) — 2m tiling via material
````
