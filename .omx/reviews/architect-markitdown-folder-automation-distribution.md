# Architect Review: MarkItDown Folder Automation Distribution

## Verdict
APPROVE

## Summary
The plan preserves the v1 boundaries and distribution goals. Source mode remains the primary debuggable path, while macOS and Windows are handled through OS-specific PyInstaller `onedir` builds.

## Strongest Steelman Antithesis
`onedir` can feel less like a polished distribution artifact than a single executable. Windows users may expect one `.exe`, and sharing or moving a folder can accidentally drop supporting files.

## Tradeoff Tension
| Option | Pros | Cons |
| --- | --- | --- |
| Source + `onedir` | Easier debugging, realistic OS-specific builds, dependency issues are visible | Folder artifact is less clean than one executable |
| `onefile` | Easier to share | More startup/extraction/debug risk for a dependency-heavy converter |

## Synthesis Path
Proceed to Critic review, but strengthen the README build section so it shows both wrapper scripts and the underlying PyInstaller command:

```bash
pyinstaller --onedir --name mark-down mark_down.py
```

```powershell
pyinstaller --onedir --name mark-down mark_down.py
```

## Recommendations Applied
- Add underlying PyInstaller commands to the README draft.
- Keep `onefile` as a roadmap item, not the v1 default.
