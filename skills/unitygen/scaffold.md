# Unity Scaffold

Design architecture and produce a compilable Unity skeleton: folder layout, `STRUCTURE.md`, C# stubs, scenes (via MCP or assets on disk). Defines *what exists and how it connects* — not full gameplay.

## Workflow

1. Read `reference.png` and game description (or change request).
2. Assess state: new project, reset, or incremental (merge with existing `STRUCTURE.md`).
3. Design scenes, prefabs, scripts, input, physics layers, render pipeline alignment (do not rip out existing URP/HDRP without cause).
4. Write `STRUCTURE.md` in full every time.
5. Create **folders** under `Assets/` as needed: `Scenes`, `Scripts`, `Prefabs`, `Materials`, `Models`, `Textures`, `Settings` — match project conventions if already present.
6. **C# stubs** — one file per new script: class name matches file name, `MonoBehaviour` (or `ScriptableObject` if data), empty `Start`/`Update` or minimal hooks, `SerializeField` fields declared where architecture implies them.
7. **Scenes** — use Unity MCP `manage_scene` (create/load/save) and `manage_gameobject` / `manage_components` to build hierarchy, OR write minimal scene YAML only if you can do so safely; prefer MCP when Editor is connected.
8. **Import assets** — copy generated files under `Assets/...`; Unity imports automatically. For large batches, allow refresh then `read_console` for import errors.
9. **Verify** — `read_console` must show no compile errors. Fix until clean.
10. **Git** — `git add -A && git commit -m "scaffold: Unity skeleton"`

## STRUCTURE.md format

````markdown
# {Project Name}

## Dimension: {2D or 3D}

## Render pipeline

{Built-in | URP | HDRP — as detected or chosen}

## Input

{Input System actions or legacy axis names — table}

## Scenes

### Main
- **File:** Assets/Scenes/Main.unity
- **Purpose:** Bootstraps game loop, loads sub-scenes or core objects

### ...
````

Per script block:

````markdown
## Scripts

### PlayerController
- **File:** Assets/Scripts/PlayerController.cs
- **Base:** MonoBehaviour
- **On:** Player prefab / root object
- **Notes:** movement, jump; reads Input action `Move`
````

## Signal / event map

Describe C# events, UnityEvents, or message names between systems — whatever the project uses.

## Asset Hints

List models, textures, audio roles for the asset planner (no style essay).

## .gitignore (project root)

Typical Unity (adjust if project already has one):

```
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Ll]ogs/
[Uu]ser[Ss]ettings/
*.csproj
*.unityproj
*.sln
*.suo
*.tmp
*.user
*.userprefs
*.pidb
*.booproj
*.svd
*.pdb
*.mdb
*.opendb
*.VC.db
```

Also ignore pipeline artifacts per `publish.sh` / `teleforge.md` (e.g. `.claude`, `screenshots`, generated `assets` if policy says so).

## Unity MCP checklist

- `set_active_instance` if multiple editors.
- After **any** script write: `read_console`.
- Large hierarchies: paged `get_hierarchy`.
- New scenes: include **Camera** and **main directional light** for 3D unless project template already provides global lighting-only setup.

## Rules

1. One primary dimension (2D vs 3D) per game flow unless explicitly hybrid.
2. Input definitions in `STRUCTURE.md` must match what stubs reference.
3. Do not leave duplicate `AudioListener` on multiple cameras in the same view.

## What NOT to Include

- Full gameplay implementation
- Task ordering (that is `PLAN.md`)
