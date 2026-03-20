# Asset Generator

PNG images via **OpenRouter** (models with image output). GLB via **Tripo3D** (unchanged).

## Environment

- `OPENROUTER_API_KEY` — required for images and for `unity-task` VQA (vision uses a separate model).
- `OPENROUTER_IMAGE_MODEL` — optional; default `google/gemini-3.1-flash-image-preview` in tools.
- `OPENROUTER_VISION_MODEL` — optional; used by `../unity-task/scripts/visual_qa.py`.
- `OPENROUTER_SITE_URL`, `OPENROUTER_APP_NAME` — optional OpenRouter attribution headers.
- `OPENROUTER_IMAGE_SIZE_512` — optional override for `--size 512` → OpenRouter `image_size` (default `0.5K` for Gemini).
- `TRIPO3D_API_KEY` — required for `glb` subcommand.

Install: `pip install -r ${CLAUDE_SKILL_DIR}/tools/requirements.txt`

## CLI

Run from project root. Tools: `${CLAUDE_SKILL_DIR}/tools/`.

### Image

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/asset_gen.py image \
  --prompt "the full prompt" -o assets/img/car.png
```

`--size`: `512`, `1K`, `2K`, `4K` (budget table below). `--aspect-ratio`: same set as before (`16:9`, `1:1`, …).

### rembg, spritesheet, slice, glb, set_budget

Sprite sheet, rembg, slice, GLB, and budget subcommands behave like the historical asset-gen skill:

- `rembg_matting.py`, `spritesheet_slice.py` unchanged in behavior
- `asset_gen.py spritesheet`, `glb`, `set_budget`

### Output

JSON on stdout; stderr for progress.

## Cost table (budget tracking)

Approximate ledger entries — real OpenRouter cost depends on model and provider.

| Operation | Preset | Cents |
|-----------|--------|-------|
| Image | 512 | 5 |
| Image | 1K | 7 |
| Image | 2K | 10 |
| Image | 4K | 15 |
| Sprite sheet | 1K 1:1 | 7 |
| GLB | medium | 30 |
| GLB | lowpoly/high/ultra | per QUALITY_PRESETS in asset_gen.py |

## Prompt cheatsheet

Unchanged rules: no “transparent background” in image prompts — solid color + `rembg_matting.py` when needed; Tripo3D ref = studio white/gray bg, no rembg before GLB.
