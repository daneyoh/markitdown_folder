# Test Spec: MarkItDown Folder Automation Distribution

## Status
Approved by Ralplan Architect/Critic consensus.

## Test Strategy
Use fast unit tests for core file-routing behavior and fake conversion, then add OS-specific smoke checks for package scripts.

## Unit Tests
1. `supported_extensions`
   - Given supported extensions, each is accepted.
   - Given unsupported extensions, each is skipped.

2. `scan_root_only`
   - Files in the input folder root are considered.
   - Files under nested folders are ignored in v1.
   - Hidden files and generated folders are skipped.

3. `collision_safe_path`
   - Existing `report.md` causes `report-001.md`.
   - Existing `report.md` and `report-001.md` cause `report-002.md`.
   - Same policy applies to moved originals in `processed/<extension>/`.

4. `successful_conversion_moves_source`
   - Fake converter returns Markdown.
   - Markdown is written under `markdown/<extension>/`.
   - Original source moves to `processed/<extension>/`.

5. `failed_conversion_keeps_source`
   - Fake converter raises an error.
   - No Markdown output is written.
   - Original source remains in place.
   - Error is logged to `logs/conversions.jsonl`.

6. `dry_run`
   - Planned actions are printed or returned.
   - No Markdown output is written.
   - No source file is moved.

7. `readme_contract`
   - README contains macOS setup, Windows setup, purpose, supported formats, safety rules, and build instructions.

## Integration Tests
1. Source mode smoke test with fake converter:
   - Run `python mark_down.py --input <tmpdir>`.
   - Verify output folder shape and logs.

2. Optional real MarkItDown smoke test:
   - Requires Python 3.10+ and installed dependencies.
   - Convert a `.txt` or `.html` fixture.
   - Mark as optional so CI can skip when dependencies are unavailable.

## Packaging Smoke Tests
### macOS
- Run `scripts/build_macos.sh` on macOS with Python 3.10+ venv.
- Verify `dist/mark-down/` exists.
- Run bundled executable against a temp folder with a text fixture.

### Windows
- Run `scripts/build_windows.ps1` on Windows with Python 3.10+ venv.
- Verify `dist\\mark-down\\` exists.
- Run bundled executable against a temp folder with a text fixture.

## Release Verification
- Source ZIP includes `README.md`, `mark_down.py`, `requirements.txt`, scripts, and tests.
- macOS package is built on macOS.
- Windows package is built on Windows.
- Each package includes a short `README.md` or points to root README.
- No package contains test input files with private data.

## Known Test Gaps
- Real PDF/DOCX/PPTX/XLSX conversion quality depends on MarkItDown and should be manually sampled after dependency installation.
- Public macOS Gatekeeper and Windows SmartScreen behavior cannot be fully validated without signing/notarization workflow.
