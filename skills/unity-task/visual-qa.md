# Visual Quality Assurance

Requires `OPENROUTER_API_KEY` and `OPENROUTER_VISION_MODEL` (or default in `unitygen/tools/openrouter_media.py`). Script resolves `unitygen/tools` for the shared OpenRouter helper.

## Static mode

```bash
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --context "Goal: ...\nRequirements: ...\nVerify: ..." \
  reference.png screenshots/{task}/main_view.png > visual-qa/${N}.md
```

## Dynamic mode

Subsampling: e.g. every 5th frame if capture was 10 FPS → 2 FPS equivalent.

```bash
mkdir -p visual-qa
N=$(ls visual-qa/*.md 2>/dev/null | wc -l); N=$((N + 1))
STEP=5
FRAMES=$(ls screenshots/{task}/*.png | awk "NR % $STEP == 0")
python3 ${CLAUDE_SKILL_DIR}/scripts/visual_qa.py \
  --context "Goal: ...\nRequirements: ...\nVerify: ..." \
  reference.png $FRAMES > visual-qa/${N}.md
```

## Failures

On **fail**, fix and re-capture up to 3 cycles; then escalate to the orchestrator with the VQA markdown content.
