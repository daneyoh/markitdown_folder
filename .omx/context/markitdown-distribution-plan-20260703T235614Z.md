# Ralplan Context: MarkItDown Folder Automation Distribution

## Task Statement
Plan the implementation and distribution approach for a local Python MarkItDown-based folder-to-Markdown automation tool. The user explicitly wants deployment planning, README purpose/usage documentation, and both macOS and Windows deliverables.

## Desired Outcome
Create consensus-ready planning artifacts that cover:
- product purpose,
- README contents,
- macOS usage and build flow,
- Windows usage and build flow,
- packaging/distribution strategy,
- tests and verification gates.

## Known Facts / Evidence
- Prior deep-interview spec exists at `.omx/specs/deep-interview-markitdown-folder-automation.md`.
- Current workspace is `/Users/donghoon/Desktop/Work_W_Claude/mark_down`.
- Workspace is currently not a git repository and contains only `.omx` planning artifacts.
- Observed local `python3` is `Python 3.9.6`.
- MarkItDown requires Python 3.10+ and recommends a virtual environment.
- MarkItDown supports optional dependencies by format, including `pdf`, `docx`, `pptx`, and `xlsx`.
- MarkItDown security guidance warns that conversion runs with current process privileges and recommends narrow local conversion APIs for local-only use.
- PyInstaller 6.21.0 documentation says `pyinstaller myscript.py` creates `build` and `dist`, and the bundled app in `dist` is what is distributed.
- PyInstaller supports `--onedir` as the default one-folder bundle and `--onefile` as a single executable.
- PyInstaller multi-OS support requires building in each target OS environment; use a venv with Python, dependencies, and PyInstaller in each environment.

## Constraints
- Do not install dependencies during planning.
- Do not create or replace Python runtime during planning.
- Do not delete files.
- Keep v1 one-shot and local-only.
- Support macOS and Windows distribution paths.
- Keep OCR/audio/URL/YouTube/LLM/cloud out of v1.

## Unknowns / Open Questions
- Whether final distribution should prefer `.zip` source package, PyInstaller `onedir`, or `onefile`.
- Whether future users are comfortable with terminal commands or need double-click wrappers.
- Whether code signing/notarization is required for public macOS distribution.

## Likely Codebase Touchpoints
- `mark_down.py`
- `README.md`
- `requirements.txt`
- `pyproject.toml`
- `scripts/build_macos.sh`
- `scripts/build_windows.ps1`
- `scripts/run_macos.sh`
- `scripts/run_windows.bat`
- `tests/test_mark_down.py`
- `.github/workflows/build.yml` only if CI release automation is later requested.

## External Evidence Sources
- MarkItDown README: https://github.com/microsoft/markitdown
- PyInstaller usage docs: https://pyinstaller.org/en/stable/usage.html
