# C# / Unity Patterns

- **MonoBehaviour** — game logic on components; use `SerializeField` for inspector fields instead of public when exposing to designers.
- **Lifecycle** — `Awake` / `Start` / `Update` / `FixedUpdate` for physics; avoid heavy work in `Update` when events or coroutines suffice.
- **References** — prefer serialized references or `GetComponent` in `Awake`/`Start`; avoid `Find` every frame.
- **Null** — Unity fake-null on destroyed objects; use explicit null checks where lifetime matters.
- **Namespaces** — match project style; default `Assets/Scripts` often uses global namespace or a single game namespace.
- **API** — for unfamiliar APIs use Unity Scripting Reference and Manual; do not invent Godot-style APIs.
