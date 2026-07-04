# Execution Spec: MarkItDown Folder Automation

## Metadata
- Source interview: `.omx/interviews/markitdown-folder-automation-20260703T235214Z.md`
- Context snapshot: `.omx/context/markitdown-folder-automation-20260703T231714Z.md`
- Profile: standard
- Final ambiguity: 14%
- Threshold: 20%
- Context type: greenfield

## Intent
Build a simple local Python tool that lets DH drop mixed document files into a folder, run one command, and receive Markdown outputs organized by original file type.

## Desired Outcome
From `/Users/donghoon/Desktop/Work_W_Claude/mark_down`, the user can run a Python command that:
- scans the current folder for supported source files,
- converts each supported file to Markdown using MarkItDown,
- writes Markdown into format-specific output folders,
- moves successfully converted source files to `processed/`,
- never overwrites existing files,
- prints a clear conversion summary.

## In Scope
- One-shot manual command only.
- Default input directory: current working directory.
- Non-recursive scan of files directly inside the input directory.
- Supported source extensions:
  - `pdf`
  - `docx`
  - `pptx`
  - `xlsx`
  - `html`
  - `txt`
  - `csv`
  - `json`
  - `xml`
- Output folder structure:
  - `markdown/<extension>/<source-stem>.md`
  - `processed/<extension>/<original-filename>`
  - `logs/conversions.jsonl`
- Use MarkItDown's local-file conversion path; prefer `convert_local()` where available.
- Create dependency files and install instructions, but do not install dependencies automatically.
- Include tests for routing, collision handling, and source movement behavior without requiring MarkItDown installation.

## Out of Scope / Non-goals
- No resident folder watcher.
- No automatic trigger when Finder opens the folder.
- No automatic trigger when terminal enters the folder.
- No recursive folder crawl in v1.
- No overwrite of Markdown or moved originals.
- No OCR.
- No audio transcription.
- No image conversion as a primary v1 target.
- No YouTube, URL, or remote-resource conversion.
- No LLM, OpenAI, Azure, or cloud integration.
- No dependency installation during implementation unless explicitly requested later.
- No deletion of source files.

## Decision Boundaries
The implementation may decide:
- exact Python file/module names,
- exact CLI option names,
- exact log field names,
- whether to use `pyproject.toml`, `requirements.txt`, or both,
- small internal helper structure,
- conservative skip rules for hidden files and generated folders.

The implementation must not decide without confirmation:
- installing packages from the network,
- creating or replacing a Python runtime,
- deleting files,
- changing v1 into a watcher or Finder automation,
- adding OCR/audio/URL/cloud/LLM behavior,
- broadening source scanning to recursive mode by default.

## Constraints
- MarkItDown requires Python 3.10+.
- The current system `python3` observed in this workspace is `Python 3.9.6`.
- MarkItDown should be installed by the user later in a Python 3.10+ virtual environment.
- Source movement happens only after Markdown output is successfully written.
- Failed conversions leave the source file in place and write an error record to the log.
- Existing files are never overwritten. Collision behavior uses numeric suffixes:
  - `report.md`
  - `report-001.md`
  - `report-002.md`

## Proposed Project Files
- `mark_down.py`: CLI entry point and orchestration.
- `requirements.txt`: minimal MarkItDown dependency declaration.
- `README.md`: Korean usage guide and install steps.
- `tests/test_mark_down.py`: tests for scan, folder routing, no-overwrite, and successful-source movement.

## CLI Shape
Default:

```bash
python mark_down.py
```

Optional flags:

```bash
python mark_down.py --input /path/to/folder --output markdown --processed processed --dry-run
```

## Acceptance Criteria
1. Running the command scans only supported files in the target folder root.
2. Unsupported files are skipped and logged as skipped.
3. Hidden files and generated folders (`markdown`, `processed`, `logs`, `.omx`, `.venv`) are skipped.
4. Each successful conversion writes Markdown to `markdown/<extension>/`.
5. Each successful source file moves to `processed/<extension>/`.
6. Failed conversions do not move the source file.
7. Existing destination files are never overwritten.
8. Duplicate output names receive numeric suffixes.
9. A dry-run mode shows planned actions without writing Markdown or moving files.
10. Tests pass without requiring real MarkItDown by using an injected or fake converter.
11. README explains Python 3.10+ requirement and installation command.

## Suggested Dependency Declaration
Use one of these forms, subject to implementation judgment:

```text
markitdown[pdf,docx,pptx,xlsx]
```

or a `pyproject.toml` dependency equivalent.

Text-based formats such as `txt`, `csv`, `json`, `xml`, and `html` may not require extra MarkItDown optional packages beyond the base package, but implementation should keep the dependency declaration conservative and documented.

## Verification Plan
- Unit test collision-safe path generation.
- Unit test supported/unsupported extension classification.
- Unit test output folder routing by extension.
- Unit test successful source movement using a fake converter.
- Unit test failed conversion leaves source in place.
- Unit test dry-run does not write or move.
- Syntax check with available local Python, acknowledging that full MarkItDown runtime requires Python 3.10+.

## Residual Risks
- Full end-to-end MarkItDown conversion cannot be verified with the observed system `python3` 3.9.6.
- Real conversion quality depends on MarkItDown's parser behavior for each file type.
- Large PDFs or Office files can still consume CPU/RAM during conversion, but the one-shot model avoids idle background resource use.

## Execution Handoff
Recommended next step: implement directly from this spec, or run `$ralplan` first if a separate plan artifact is desired.
