# PRD: MarkItDown Folder Automation Distribution

## Status
Approved by Ralplan Architect/Critic consensus.

## Background
DH wants a local Python utility that converts files dropped into a folder into Markdown, grouped by original file type. A deep-interview already fixed the v1 product boundaries: one-shot manual execution, local files only, no overwrites, successful originals moved to `processed/`, and no OCR/audio/URL/LLM/cloud behavior.

The new planning requirement adds deployment and documentation: the tool should be understandable from a README and distributable for both macOS and Windows.

## Goals
- Build a simple local CLI tool: `python mark_down.py`.
- Provide clear Korean README documentation covering purpose, install, usage, output folders, safety rules, troubleshooting, and Mac/Windows paths.
- Provide source-based use for users who can install Python 3.10+.
- Provide package/build scripts for macOS and Windows.
- Avoid installing dependencies or building binaries during planning.

## Non-goals
- No resident watcher.
- No Finder/Explorer folder-open automation.
- No recursive scan by default.
- No cloud/LLM/OCR/audio/URL conversion.
- No cross-compiling Windows executable from macOS or macOS executable from Windows.
- No code signing/notarization in v1, but document it as a public-release follow-up.
- No auto-update system.

## Target Users
- Primary: DH, running locally on macOS.
- Secondary: Windows users who receive a release package and run the same one-shot behavior.
- Assumption: Users can run a terminal command or a simple `.bat`/`.sh` wrapper.

## Product Behavior
1. User places supported files in a folder.
2. User runs the tool in that folder.
3. Tool scans only the folder root.
4. Tool skips generated folders and hidden files.
5. Tool converts supported files to Markdown.
6. Tool writes results to `markdown/<extension>/`.
7. Tool moves successfully converted originals to `processed/<extension>/`.
8. Tool writes JSONL logs to `logs/conversions.jsonl`.
9. Tool never overwrites existing outputs or moved originals.
10. Tool reports summary counts: converted, skipped, failed, moved.

## Supported Formats
- `pdf`
- `docx`
- `pptx`
- `xlsx`
- `html`
- `txt`
- `csv`
- `json`
- `xml`

## Distribution Requirements
### Source Distribution
- Include `mark_down.py`, `requirements.txt`, `README.md`, and tests.
- README provides macOS and Windows setup commands.
- User installs Python 3.10+ and dependencies manually.

### macOS Distribution
- Provide `scripts/run_macos.sh` for source mode.
- Provide `scripts/build_macos.sh` for PyInstaller build mode.
- Build output should be `dist/mark-down/` using PyInstaller `onedir` by default.
- Public distribution may later need signing/notarization; v1 documents this as a follow-up rather than implementing it.

### Windows Distribution
- Provide `scripts/run_windows.bat` or `scripts/run_windows.ps1` for source mode.
- Provide `scripts/build_windows.ps1` for PyInstaller build mode.
- Build output should be `dist/mark-down/` using PyInstaller `onedir` by default.
- Windows executable must be built on Windows, or in a Windows VM/CI runner.

## README Requirements
README must include:
- Tool name and one-sentence purpose.
- Why this exists.
- What it does and does not do.
- Supported formats.
- Folder structure before/after.
- macOS setup and run commands.
- Windows setup and run commands.
- Build/package commands for macOS and Windows.
- Safety rules: no overwrite, successful-source move only, failed files stay in place.
- Troubleshooting: Python version, MarkItDown import failure, permission errors, unsupported files.
- Known limitations and roadmap.

## Acceptance Criteria
1. README has separate macOS and Windows setup/run/build sections.
2. README explains the product purpose in Korean.
3. README documents output folders and source movement policy.
4. README states Python 3.10+ is required.
5. README includes `requirements.txt` install command.
6. README includes PyInstaller packaging command for macOS.
7. README includes PyInstaller packaging command for Windows.
8. Plan explicitly states OS-specific builds are required for OS-specific binaries.
9. Implementation plan includes tests that do not require MarkItDown installation.
10. Implementation plan includes release verification for both source mode and packaged mode.

## Risks
- MarkItDown dependency tree may be large for packaged binaries.
- PyInstaller may need hidden imports or metadata collection for MarkItDown dependencies.
- macOS Gatekeeper may block unsigned binaries in public distribution.
- Windows antivirus may flag unsigned PyInstaller executables.
- Current local `python3` is 3.9.6, so local full runtime verification requires a Python 3.10+ environment.

## References
- MarkItDown README: https://github.com/microsoft/markitdown
- PyInstaller usage: https://pyinstaller.org/en/stable/usage.html
