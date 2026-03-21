#!/usr/bin/env python3

import io
import os
import sys
from pathlib import Path

from PIL import Image

_SKILLS_ROOT = Path(__file__).resolve().parents[2]
_TOOLS = _SKILLS_ROOT / "unitygen" / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from dotenv_loader import load_dotenv_from_tree
from openrouter_media import chat_completions, default_vision_model, extract_assistant_text, png_bytes_to_data_url

STATIC_PROMPT = Path(__file__).parent / "static_prompt.md"
DYNAMIC_PROMPT = Path(__file__).parent / "dynamic_prompt.md"


def _maybe_downscale_png(data: bytes, max_side: int) -> bytes:
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    w, h = img.size
    m = max(w, h)
    if m <= max_side:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    scale = max_side / m
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main():
    load_dotenv_from_tree()
    args = sys.argv[1:]
    context = None
    if len(args) >= 2 and args[0] == "--context":
        context = args[1]
        args = args[2:]

    if len(args) < 2:
        print(
            f"Usage: {sys.argv[0]} [--context \"task context\"] <reference.png> <screenshot.png> [frame2.png ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    paths = [Path(p) for p in args]
    for p in paths:
        if not p.exists():
            print(f"Error: {p} not found", file=sys.stderr)
            sys.exit(1)

    max_side = int(os.environ.get("OPENROUTER_VQA_MAX_SIDE", "2048"))
    static = len(paths) == 2
    prompt = (STATIC_PROMPT if static else DYNAMIC_PROMPT).read_text(encoding="utf-8")
    if context:
        prompt += f"\n\n## Task Context\n\n{context}\n"

    content: list[dict] = [{"type": "text", "text": prompt}]
    content.append({"type": "text", "text": "Reference (visual target):"})
    ref_bytes = _maybe_downscale_png(paths[0].read_bytes(), max_side)
    content.append({"type": "image_url", "image_url": {"url": png_bytes_to_data_url(ref_bytes)}})

    if static:
        content.append({"type": "text", "text": "Game screenshot:"})
        ss = _maybe_downscale_png(paths[1].read_bytes(), max_side)
        content.append({"type": "image_url", "image_url": {"url": png_bytes_to_data_url(ss)}})
        desc = "static (reference + screenshot)"
    else:
        for i, p in enumerate(paths[1:], 1):
            content.append({"type": "text", "text": f"Frame {i}:"})
            fb = _maybe_downscale_png(p.read_bytes(), max_side)
            content.append({"type": "image_url", "image_url": {"url": png_bytes_to_data_url(fb)}})
        desc = f"dynamic (reference + {len(paths) - 1} frames)"

    model = os.environ.get("OPENROUTER_VISION_MODEL") or default_vision_model()
    print(f"Analyzing {desc} with OpenRouter ({model})...", file=sys.stderr)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
    }

    try:
        data = chat_completions(payload)
    except Exception as e:
        print(f"Error: OpenRouter API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    text = extract_assistant_text(data)
    if not text:
        print("Error: model returned no text (possible safety block)", file=sys.stderr)
        sys.exit(1)

    print(text)


if __name__ == "__main__":
    main()
