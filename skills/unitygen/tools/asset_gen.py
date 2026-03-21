#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

from openrouter_media import (
    chat_completions,
    default_image_model,
    extract_first_generated_png,
    png_bytes_to_data_url,
)
from dotenv_loader import load_dotenv_from_tree
from tripo3d import MODEL_V3, image_to_glb

TOOLS_DIR = Path(__file__).parent
TEMPLATE_SCRIPT = TOOLS_DIR / "spritesheet_template.py"
BUDGET_FILE = Path("assets/budget.json")


def _load_budget():
    if not BUDGET_FILE.exists():
        return None
    return json.loads(BUDGET_FILE.read_text())


def _spent_total(budget):
    return sum(v for entry in budget.get("log", []) for v in entry.values())


def check_budget(cost_cents: int):
    budget = _load_budget()
    if budget is None:
        return
    spent = _spent_total(budget)
    remaining = budget.get("budget_cents", 0) - spent
    if cost_cents > remaining:
        result_json(
            False,
            error=f"Budget exceeded: need {cost_cents}¢ but only {remaining}¢ remaining ({spent}¢ of {budget['budget_cents']}¢ spent)",
        )
        sys.exit(1)


def record_spend(cost_cents: int, service: str):
    budget = _load_budget()
    if budget is None:
        return
    budget.setdefault("log", []).append({service: cost_cents})
    BUDGET_FILE.write_text(json.dumps(budget, indent=2) + "\n")


SPRITESHEET_SYSTEM_TPL = """\
Using the attached template image as an exact layout guide: generate a sprite sheet.
The image is a 4x4 grid of 16 equal cells separated by red lines.
Replace each numbered cell with the corresponding content, reading left-to-right, top-to-bottom (cell 1 = first, cell 16 = last).

Rules:
- KEEP the red grid lines exactly where they are in the template — do not remove, shift, or paint over them
- Each cell's content must be CENTERED in its cell and must NOT cross into adjacent cells
- CRITICAL: fill ALL empty space in every cell with flat solid {bg_color} — no gradients, no scenery, no patterns, just the plain color
- Maintain consistent style, lighting direction, and proportions across all 16 cells
- CRITICAL: do NOT draw the numbered circles from the template onto the output — replace them entirely with the actual drawing content"""

QUALITY_PRESETS = {
    "lowpoly": {
        "face_limit": 5000,
        "smart_low_poly": True,
        "texture_quality": "standard",
        "geometry_quality": "standard",
        "cost_cents": 40,
    },
    "medium": {
        "face_limit": 20000,
        "smart_low_poly": False,
        "texture_quality": "standard",
        "geometry_quality": "standard",
        "cost_cents": 30,
    },
    "high": {
        "face_limit": None,
        "smart_low_poly": False,
        "texture_quality": "detailed",
        "geometry_quality": "standard",
        "cost_cents": 40,
    },
    "ultra": {
        "face_limit": None,
        "smart_low_poly": False,
        "texture_quality": "detailed",
        "geometry_quality": "detailed",
        "cost_cents": 60,
    },
}


def result_json(ok: bool, path: str | None = None, cost_cents: int = 0, error: str | None = None):
    d = {"ok": ok, "cost_cents": cost_cents}
    if path:
        d["path"] = path
    if error:
        d["error"] = error
    print(json.dumps(d))


IMAGE_SIZES = ["512", "1K", "2K", "4K"]
IMAGE_COSTS = {"512": 5, "1K": 7, "2K": 10, "4K": 15}
IMAGE_ASPECT_RATIOS = ["1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"]


def _openrouter_image_size(size_key: str) -> str:
    if size_key == "512":
        return os.environ.get("OPENROUTER_IMAGE_SIZE_512", "0.5K")
    return size_key


def cmd_image(args):
    size = args.size
    cost = IMAGE_COSTS[size]
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    model = os.environ.get("OPENROUTER_IMAGE_MODEL") or default_image_model()
    or_size = _openrouter_image_size(size)
    label = f"{or_size} {args.aspect_ratio}"
    print(f"Generating image ({label}) via OpenRouter...", file=sys.stderr)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": args.prompt}],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": args.aspect_ratio,
            "image_size": or_size,
        },
    }

    try:
        data = chat_completions(payload)
        png = extract_first_generated_png(data)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    output.write_bytes(png)
    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "openrouter_image")
    result_json(True, path=str(output), cost_cents=cost)


def generate_template(bg_color: str) -> bytes:
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp = f.name
    subprocess.run(
        [sys.executable, str(TEMPLATE_SCRIPT), "-o", tmp, "--bg", bg_color],
        check=True,
        capture_output=True,
    )
    data = Path(tmp).read_bytes()
    Path(tmp).unlink()
    return data


def cmd_spritesheet(args):
    cost = IMAGE_COSTS["1K"]
    check_budget(cost)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    bg = args.bg
    template_bytes = generate_template(bg)
    system = SPRITESHEET_SYSTEM_TPL.format(bg_color=bg)
    print(f"Generating sprite sheet (bg={bg}) via OpenRouter...", file=sys.stderr)
    model = os.environ.get("OPENROUTER_IMAGE_MODEL") or default_image_model()

    tpl_url = png_bytes_to_data_url(template_bytes)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": tpl_url}},
                    {"type": "text", "text": args.prompt},
                ],
            },
        ],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": "1:1", "image_size": "1K"},
    }

    try:
        data = chat_completions(payload)
        png = extract_first_generated_png(data)
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    output.write_bytes(png)
    print(f"Saved: {output}", file=sys.stderr)
    record_spend(cost, "openrouter_image")
    result_json(True, path=str(output), cost_cents=cost)


def cmd_glb(args):
    image_path = Path(args.image)
    if not image_path.exists():
        result_json(False, error=f"Image not found: {image_path}")
        sys.exit(1)

    preset = QUALITY_PRESETS.get(args.quality, QUALITY_PRESETS["medium"])
    check_budget(preset["cost_cents"])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting to GLB (quality={args.quality})...", file=sys.stderr)

    try:
        image_to_glb(
            image_path,
            output,
            model_version=MODEL_V3,
            face_limit=preset["face_limit"],
            smart_low_poly=preset["smart_low_poly"],
            texture_quality=preset["texture_quality"],
            geometry_quality=preset["geometry_quality"],
        )
    except Exception as e:
        result_json(False, error=str(e))
        sys.exit(1)

    print(f"Saved: {output}", file=sys.stderr)
    record_spend(preset["cost_cents"], "tripo3d")
    result_json(True, path=str(output), cost_cents=preset["cost_cents"])


def cmd_set_budget(args):
    BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    budget = {"budget_cents": args.cents, "log": []}
    if BUDGET_FILE.exists():
        old = json.loads(BUDGET_FILE.read_text())
        budget["log"] = old.get("log", [])
    BUDGET_FILE.write_text(json.dumps(budget, indent=2) + "\n")
    spent = _spent_total(budget)
    print(json.dumps({"ok": True, "budget_cents": args.cents, "spent_cents": spent, "remaining_cents": args.cents - spent}))


def main():
    load_dotenv_from_tree()
    parser = argparse.ArgumentParser(description="Asset Generator — images (OpenRouter) and GLBs (Tripo3D)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="Generate a PNG image")
    p_img.add_argument("--prompt", required=True, help="Full image generation prompt")
    p_img.add_argument(
        "--size",
        choices=IMAGE_SIZES,
        default="1K",
        help="Resolution key: 512→0.5K (Gemini), 1K, 2K, 4K",
    )
    p_img.add_argument("--aspect-ratio", choices=IMAGE_ASPECT_RATIOS, default="1:1", help="Aspect ratio")
    p_img.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_img.set_defaults(func=cmd_image)

    p_ss = sub.add_parser("spritesheet", help="Generate 4x4 sprite sheet")
    p_ss.add_argument("--prompt", required=True, help="Animation or item list subject")
    p_ss.add_argument("--bg", default="#00FF00", help="Background color hex")
    p_ss.add_argument("-o", "--output", required=True, help="Output PNG path")
    p_ss.set_defaults(func=cmd_spritesheet)

    p_glb = sub.add_parser("glb", help="Convert PNG to GLB 3D model")
    p_glb.add_argument("--image", required=True, help="Input PNG path")
    p_glb.add_argument("--quality", default="medium", choices=list(QUALITY_PRESETS.keys()), help="Quality preset")
    p_glb.add_argument("-o", "--output", required=True, help="Output GLB path")
    p_glb.set_defaults(func=cmd_glb)

    p_budget = sub.add_parser("set_budget", help="Set asset budget in cents")
    p_budget.add_argument("cents", type=int, help="Budget in cents")
    p_budget.set_defaults(func=cmd_set_budget)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
