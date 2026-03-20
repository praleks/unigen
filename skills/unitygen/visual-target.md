# Visual Target

Generate a reference image of the finished game. Anchors art direction for scaffold, asset planner, and task agents.

## CLI

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "{prompt}" \
  --size 1K --aspect-ratio 16:9 -o reference.png
```

Requires `OPENROUTER_API_KEY` and a model with image output (`OPENROUTER_IMAGE_MODEL` optional).

## Prompt

Must read like an in-game screenshot, not concept art:

```
Screenshot of a {genre} {2D/3D} video game. {Key gameplay moment — peak action, not a menu}. {Environment details}. {Art style — be specific and bold}. In-game camera perspective, HUD visible. Clean digital rendering, game engine output.
```

## Output

`reference.png` — default 1K 16:9.

Seed `ASSETS.md`:

```markdown
# Assets

**Art direction:** <the art style description>
```
