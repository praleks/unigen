# Unity Quirks

- **Script compilation** — domain reload after edits; poll `read_console` and `editor_state` if available. Do not attach behaviours until scripts compile.
- **Scene dirty state** — save scenes (`manage_scene` save) after meaningful hierarchy or component changes.
- **Prefab overrides** — changing a prefab instance can create overrides; know whether to apply to prefab or edit the prefab asset.
- **Input** — project may use Input System package or legacy Input; follow `STRUCTURE.md` and existing project code.
- **Camera** — new scenes need Camera and main Light for meaningful screenshots; match pipeline (URP/HDRP/Built-in) already in the project.
- **Physics timestep** — low frame captures can miss collisions; use adequate play duration before screenshots for motion tasks.
- **Paths** — MCP paths are usually under `Assets/` with forward slashes.
