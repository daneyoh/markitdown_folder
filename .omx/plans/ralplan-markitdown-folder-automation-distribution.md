# Ralplan: MarkItDown Folder Automation Distribution

## Status
Approved by Architect and Critic.

## Inputs
- Deep-interview spec: `.omx/specs/deep-interview-markitdown-folder-automation.md`
- Context snapshot: `.omx/context/markitdown-distribution-plan-20260703T235614Z.md`
- PRD: `.omx/plans/prd-markitdown-folder-automation-distribution.md`
- Test spec: `.omx/plans/test-spec-markitdown-folder-automation-distribution.md`

## RALPLAN-DR Summary
### Principles
1. Keep v1 local, explicit, and reversible except for the user-approved successful-source move to `processed/`.
2. Separate product implementation from distribution packaging so source mode remains easy to debug.
3. Prefer documented OS-native builds over pretending one host can produce all binaries.
4. Make README the user contract: purpose, safety, usage, limitations, and release instructions must be visible.
5. Do not make the package smarter than the v1 scope: no watchers, OCR, cloud, or recursive scan.

### Decision Drivers
1. Low operational risk for personal files.
2. Easy install/use on macOS and Windows.
3. Verifiable behavior without requiring real MarkItDown in unit tests.

### Viable Options
#### Option A: Source-first + OS-specific PyInstaller `onedir` builds
Pros:
- Keeps development simple.
- Enables source users and non-Python users.
- `onedir` is easier to inspect/debug than `onefile`.
- Aligns with PyInstaller default output model.

Cons:
- Release package contains a folder, not a single binary.
- Requires separate macOS and Windows build environments.

#### Option B: PyInstaller `onefile` only
Pros:
- Single-file distribution is easier to share.
- Simpler user-facing artifact.

Cons:
- Harder to debug dependency and extraction issues.
- Large startup/extraction cost may be worse with document-conversion dependencies.
- Still requires separate OS builds.

#### Option C: Python package only
Pros:
- Smallest artifact and simplest engineering.
- Avoids PyInstaller edge cases.

Cons:
- Requires every user to install Python 3.10+ and dependencies.
- Weaker fit for "deployment" to Windows users.

### Favored Option
Option A: Source-first + OS-specific PyInstaller `onedir` builds.

## Recommended Plan
### Phase 1: Project Skeleton and Core CLI
- Create `mark_down.py` with argparse CLI.
- Create `requirements.txt` with MarkItDown format extras and PyInstaller as a dev/build dependency decision.
- Keep converter behind a small adapter so tests can inject a fake converter.
- Implement local-only, non-recursive root scan.
- Implement supported-extension routing.
- Implement collision-safe writes and moves.
- Implement JSONL logging.

### Phase 2: README and User Contract
- Create root `README.md` in Korean.
- Include purpose, supported formats, input/output examples, safety rules, macOS commands, Windows commands, packaging commands, troubleshooting, and limitations.
- State that Python 3.10+ is required.
- State that failed files stay in place and successful files move to `processed/`.

### Phase 3: macOS and Windows Runner Scripts
- Add `scripts/run_macos.sh`.
- Add `scripts/run_windows.bat` or `scripts/run_windows.ps1`.
- Scripts should call the source-mode CLI and avoid environment mutation beyond activating an existing venv when present.

### Phase 4: Packaging Scripts
- Add `scripts/build_macos.sh`.
- Add `scripts/build_windows.ps1`.
- Use PyInstaller `--onedir --name mark-down mark_down.py` by default.
- Document optional `--onefile` as a future switch, not v1 default.
- Build macOS artifacts on macOS and Windows artifacts on Windows.

### Phase 5: Tests and Release Checks
- Add unit tests with fake converter.
- Add README contract tests.
- Add optional integration smoke for real MarkItDown.
- Add release checklist covering source ZIP, macOS `dist/mark-down/`, and Windows `dist\\mark-down\\`.

## README Draft Outline
1. `# Mark Down 자동 정리 도구`
2. `## 만든 목적`
3. `## 한 줄 요약`
4. `## 지원 파일`
5. `## 폴더 구조`
6. `## macOS 설치`
7. `## macOS 실행`
8. `## Windows 설치`
9. `## Windows 실행`
10. `## 배포용 빌드`
11. `## 안전 규칙`
12. `## 문제 해결`
13. `## 제한 사항`
14. `## 향후 개선`

## Implementation File Plan
- `mark_down.py`: core CLI and orchestration.
- `requirements.txt`: runtime dependency declaration.
- `requirements-dev.txt`: test/build dependencies, including PyInstaller.
- `README.md`: product documentation.
- `scripts/run_macos.sh`: macOS source-mode helper.
- `scripts/run_windows.bat`: Windows source-mode helper.
- `scripts/build_macos.sh`: macOS PyInstaller build helper.
- `scripts/build_windows.ps1`: Windows PyInstaller build helper.
- `tests/test_mark_down.py`: behavior tests.

## Verification Steps
1. Run unit tests with fake converter.
2. Run syntax check with available Python.
3. Verify README contains all required sections.
4. On Python 3.10+ environment, run optional source-mode smoke.
5. On macOS Python 3.10+ environment, run macOS build script and bundled smoke.
6. On Windows Python 3.10+ environment, run Windows build script and bundled smoke.

## ADR
### Decision
Use source-first implementation with OS-specific PyInstaller `onedir` packaging for macOS and Windows.

### Drivers
- Safety and clarity for local document handling.
- Need to serve both Python-capable and non-Python users.
- Need a realistic cross-platform distribution path.

### Alternatives Considered
- `onefile` only: rejected as a v1 default because dependency-heavy document conversion is easier to debug in `onedir`.
- Python package only: rejected as insufficient for Windows deployment expectations.
- Watcher/Explorer/Finder automation: rejected by prior deep-interview scope.

### Why Chosen
The chosen path keeps the core tool simple, testable, and source-runnable while giving a practical package route for macOS and Windows. It also matches PyInstaller's documented default `onedir` model and avoids unsupported cross-OS build assumptions.

### Consequences
- Release workflow must run on both macOS and Windows.
- `dist/mark-down/` folders are larger than a single script.
- Later public distribution may need code signing/notarization.

### Follow-ups
- Decide whether public release requires signing.
- Add CI builds only after local scripts pass.
- Revisit `onefile` after `onedir` package is stable.

## Available-Agent-Types Roster
- `executor`: implement code/docs/scripts.
- `test-engineer`: build tests and release smoke checks.
- `writer`: refine Korean README and troubleshooting.
- `verifier`: validate artifacts and acceptance criteria.
- `architect`: review packaging boundaries and OS build assumptions.
- `critic`: final plan/code quality gate.

## Follow-up Staffing Guidance
### `$ultragoal` Default
Use `$ultragoal` for durable sequential execution:
- Goal 1: core CLI + fake-converter tests.
- Goal 2: README + Mac/Windows runner docs.
- Goal 3: packaging scripts.
- Goal 4: verification and release checklist.

### `$team` Option
Use `$team` if parallel execution is desired:
- `executor` lane: `mark_down.py`, dependency files.
- `writer` lane: `README.md`.
- `test-engineer` lane: tests and smoke strategy.
- `verifier` lane: final acceptance and release checklist.

### `$ralph` Fallback
Use `$ralph` only if a single persistent owner is preferred over durable goal tracking. It is not the recommended default here.

## Goal-Mode Follow-up Suggestions
- `$ultragoal`: recommended default for implementation.
- `$team`: useful if README/tests/packaging should happen in parallel.
- `$performance-goal`: not applicable unless package startup or conversion throughput becomes a measured target.
- `$autoresearch-goal`: not applicable; this is an implementation/distribution project, not a research mission.

## Team Launch Hints
```bash
$team .omx/plans/ralplan-markitdown-folder-automation-distribution.md
```

If using OMX CLI directly:

```bash
omx team .omx/plans/ralplan-markitdown-folder-automation-distribution.md
```

## Team Verification Path
- Team must return changed file list.
- Team must run unit tests or report exact blocker.
- Team must verify README contract.
- Team must report OS build checks as `done`, `blocked: no Python 3.10+`, or `blocked: wrong OS`.

## Best-Practice Research Notes
- MarkItDown: official README establishes Python 3.10+, venv recommendation, optional format dependencies, supported formats, and local I/O security caveats.
- PyInstaller: official docs establish `build`/`dist` output, `onedir` default, `onefile` option, venv-per-environment guidance, and OS-specific build environments for multiple operating systems.

## Consensus Changelog
- Architect review approved the plan and recommended adding underlying PyInstaller commands to the README draft.
- Applied README draft update showing `pyinstaller --onedir --name mark-down mark_down.py` for both macOS and Windows.
- Critic review approved the handoff and suggested non-blocking README examples for `--input` and `--dry-run`.
- Applied dependency-role clarification: PyInstaller belongs in `requirements-dev.txt`, while MarkItDown remains runtime dependency.
