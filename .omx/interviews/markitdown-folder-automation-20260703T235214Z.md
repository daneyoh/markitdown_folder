# Deep Interview Transcript: MarkItDown Folder Automation

## Metadata
- Profile: standard
- Context type: greenfield
- Final ambiguity: 14%
- Threshold: 20%
- Context snapshot: `.omx/context/markitdown-folder-automation-20260703T231714Z.md`
- Execution-ready spec: `.omx/specs/deep-interview-markitdown-folder-automation.md`

## Technical Context
- Workspace: `/Users/donghoon/Desktop/Work_W_Claude/mark_down`
- Workspace status: empty folder, not a git repository
- Local `python3`: `Python 3.9.6`
- MarkItDown reference: https://github.com/microsoft/markitdown
- MarkItDown requires Python 3.10+ and recommends a virtual environment.
- MarkItDown supports optional dependencies by format, for example `pdf`, `docx`, `pptx`, and `xlsx`.
- MarkItDown security notes warn that conversion runs with current process privileges and recommend narrow conversion APIs for local-only use.

## Clarity Breakdown
| Dimension | Score | Notes |
| --- | ---: | --- |
| Intent | 0.88 | User wants a low-friction local file-to-Markdown organizer. |
| Outcome | 0.88 | Run one command in a folder, get Markdown outputs grouped by source format. |
| Scope | 0.92 | One-shot local conversion only, no resident watcher. |
| Constraints | 0.88 | No overwrite, successful source files move to `processed/`, lightweight local formats only. |
| Success | 0.74 | Script, dependency files, usage docs, and tests can be verified without installing MarkItDown. |

## Readiness Gates
- Non-goals: explicit.
- Decision boundaries: explicit.
- Pressure pass: complete. The original "automatic when files arrive" idea was challenged against RAM/workload concerns and reduced to manual one-shot execution.

## Transcript
### Round 1
Question: What is the v1 operating model?

Answer: Use a manual one-shot command. No automatic trigger when entering the folder, no resident watcher.

Resulting ambiguity: 39%

### Round 2
Question: How should source files be handled?

Answer: After successful conversion, move the original file into `processed/`.

Resulting ambiguity: 30%

### Round 3
Question: How should duplicate names or reruns behave?

Answer: Do not overwrite. Append numeric suffixes such as `-001`, `-002`.

Resulting ambiguity: 24%

### Round 4
Question: Which formats are in scope?

Answer: Lightweight local document formats only: `pdf`, `docx`, `pptx`, `xlsx`, `html`, `txt`, `csv`, `json`, `xml`.

Resulting ambiguity: 18%

### Round 5
Question: How should dependencies be handled?

Answer: Create dependency declarations and install instructions, but do not install dependencies during v1.

Resulting ambiguity: 14%

## Handoff Recommendation
Proceed to implementation with the spec in `.omx/specs/deep-interview-markitdown-folder-automation.md`.
