# Deep Interview Context: MarkItDown Folder Automation

## Task Statement
User wants a Python tool, benchmarked against `microsoft/markitdown`, that watches or receives files in a folder, understands the files, and places Markdown outputs into format-specific folders.

## Desired Outcome
An execution-ready specification for a local Python automation tool that converts incoming files to Markdown and organizes converted outputs by source file type.

## Stated Solution
Build one Python script/program that uses MarkItDown-like conversion behavior.

## Probable Intent Hypothesis
The user likely wants a low-friction personal document ingestion pipeline: drop mixed files into a folder, have them converted to Markdown automatically, and keep outputs organized for later reading, search, or LLM use.

## Known Facts / Evidence
- Current workspace path: `/Users/donghoon/Desktop/Work_W_Claude/mark_down`.
- The folder is currently empty.
- The folder is not a git repository.
- Local `python3 --version` returned `Python 3.9.6`.
- MarkItDown requires Python 3.10 or higher according to its README.
- MarkItDown supports converting PDFs, PowerPoint, Word, Excel, images, audio, HTML, text-based formats, ZIP files, YouTube URLs, EPubs, and more.
- MarkItDown can be used from CLI (`markitdown path-to-file.pdf -o document.md`) or Python API (`MarkItDown().convert(...)`).
- MarkItDown performs I/O with the current process privileges, so input scope and unsafe files need explicit boundaries.

## Constraints
- Use Korean for communication.
- Do not implement directly inside deep-interview mode.
- Do not delete or overwrite files without confirmation.
- Need a plan/spec before code.
- Need Python 3.10+ environment for MarkItDown.

## Unknowns / Open Questions
- Should the tool continuously watch a folder, run once on demand, or support both?
- What exact input folder and output folder structure should be used?
- Which file formats are in scope for the first version?
- Should the original files be moved, copied, archived, or left untouched?
- How should duplicate filenames, failed conversions, and unsupported files be handled?
- Is OCR/LLM/cloud conversion allowed, or should v1 be fully local/offline?
- Should output include metadata/front matter, source path, timestamps, or conversion logs?

## Decision-Boundary Unknowns
- May the agent choose folder names and file naming conventions?
- May the agent add dependencies such as `markitdown`, `watchdog`, or `rich`?
- May the agent create a virtual environment or dependency files?
- Should destructive actions such as moving source files be prohibited in v1?

## Likely Codebase Touchpoints
- New Python script, likely `mark_down_automation.py` or similar.
- Optional `requirements.txt` / `pyproject.toml`.
- Optional `README.md` with usage.
- Optional `tests/` with sample conversion routing behavior.

## Prompt-Safe Initial-Context Summary Status
not_needed
