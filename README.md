# Mark Down 자동 정리 도구

## 만든 목적
로컬 폴더에 모아 둔 문서 파일을 한 번 실행으로 Markdown으로 변환하고, 성공한 원본은 `원본완료/`로 옮겨 폴더를 정리하기 위한 도구입니다.

## 한 줄 요약
`python bin/mark_down.py --input ./input-folder`를 실행하면 지원 파일을 `변환/<형식>/`에 `.md`로 저장하고, 성공한 원본만 `원본완료/<형식>/`로 이동합니다.

## 빠른 시작
GitHub에서 ZIP으로 내려받거나 `git clone`으로 받은 뒤, 아래 순서대로 실행하세요.

```bash
git clone https://github.com/daneyoh/markitdown_folder.git
cd markitdown_folder
```

macOS:

```bash
scripts/setup_macos.sh
scripts/run_macos.sh --input /Users/you/Desktop/sample-folder --dry-run
scripts/run_macos.sh --input /Users/you/Desktop/sample-folder
```

Windows PowerShell:

```powershell
.\scripts\setup_windows.ps1
.\scripts\run_windows.bat --input C:\Users\you\Desktop\sample-folder --dry-run
.\scripts\run_windows.bat --input C:\Users\you\Desktop\sample-folder
```

## 지원 파일
- `pdf`
- `docx`
- `pptx`
- `xlsx`
- `html`
- `txt`
- `csv`
- `json`
- `xml`

지원 목록만 확인하려면:

```bash
python3 bin/mark_down.py --list-supported
```

## 폴더 구조
실행 전:

```text
work-folder/
  report.pdf
  memo.txt
  image.png
```

실행 후:

```text
work-folder/
  image.png
  변환/
    pdf/report.md
    txt/memo.md
  원본완료/
    pdf/report.pdf
    txt/memo.txt
  logs/
    conversions.jsonl
```

## macOS 설치
Python 3.10+ 환경에서 실행하세요.

```bash
cd markitdown_folder
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

또는:

```bash
scripts/setup_macos.sh
```

## macOS 실행
기본 실행:

```bash
python3 bin/mark_down.py --input /Users/you/Desktop/sample-folder
```

미리보기:

```bash
python3 bin/mark_down.py --input /Users/you/Desktop/sample-folder --dry-run
```

helper script:

```bash
scripts/run_macos.sh --input /Users/you/Desktop/sample-folder
```

## Windows 설치
Python 3.10+ 환경에서 실행하세요.

```powershell
cd C:\Users\you\Desktop\markitdown_folder
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

또는:

```powershell
.\scripts\setup_windows.ps1
```

## Windows 실행
기본 실행:

```powershell
python bin\mark_down.py --input C:\Users\you\Desktop\sample-folder
```

미리보기:

```powershell
python bin\mark_down.py --input C:\Users\you\Desktop\sample-folder --dry-run
```

helper script:

```bat
scripts\run_windows.bat --input C:\Users\you\Desktop\sample-folder
```

## 옵션
- `--input`: 한 번 스캔할 로컬 폴더입니다. 기본값은 현재 폴더입니다.
- `--output`: Markdown 출력 폴더입니다. 기본값은 `변환`입니다.
- `--processed`: 성공한 원본 이동 폴더입니다. 기본값은 `원본완료`입니다.
- `--log`: JSONL 로그 파일입니다. 기본값은 `logs/conversions.jsonl`입니다.
- `--dry-run`: 쓰기와 이동 없이 예정 작업만 출력합니다.
- `--list-supported`: 지원 확장자를 출력합니다.

## 배포용 빌드
PyInstaller는 개발/빌드 의존성이므로 빌드 환경에서는 `requirements-dev.txt`를 설치합니다.

```bash
python3 -m pip install -r requirements-dev.txt
```

v1 기본 배포 형식은 디버깅이 쉬운 `onedir`입니다. 내부 명령은 macOS와 Windows 모두 다음 형태입니다.

```bash
pyinstaller --onedir --name mark-down --icon assets/icons/mark-down.icns --paths src bin/mark_down.py
```

Windows에서는 icon 경로만 `.ico`로 바뀝니다.

```powershell
pyinstaller --onedir --name mark-down --icon assets\icons\mark-down.ico --paths src bin\mark_down.py
```

### macOS 빌드
macOS용 실행 파일은 macOS에서 빌드하세요.

```bash
scripts/build_macos.sh
```

결과물:

```text
dist/mark-down/
```

### Windows 빌드
Windows용 실행 파일은 Windows 또는 Windows VM/CI runner에서 빌드하세요.

```powershell
.\scripts\build_windows.ps1
```

결과물:

```text
dist\mark-down\
```

`--onefile` 단일 파일 배포는 v1 기본값이 아닙니다. MarkItDown 의존성이 큰 편이라 v1에서는 문제 추적이 쉬운 `onedir`을 먼저 안정화합니다.

### GitHub Actions 빌드
이 repo는 `.github/workflows/build.yml`로 macOS와 Windows 빌드를 실행합니다.

- `main` push 또는 pull request: 테스트와 OS별 PyInstaller build artifact 생성
- `v*` tag push: GitHub Release에 macOS/Windows zip 파일 업로드

## 사용자 폴더 구조
실행 파일을 폴더에 넣고 실행하면 기본 결과는 아래처럼 정리됩니다.

```text
work-folder/
  mark-down 실행파일
  변환/
    pdf/
    docx/
    xlsx/
    txt/
  원본완료/
    pdf/
    docx/
    xlsx/
    txt/
  logs/
    conversions.jsonl
```

`변환/<형식>/`에는 Markdown 결과물만 들어갑니다. 원본 파일은 `원본완료/<형식>/`에 따로 보관합니다.

## repo 구조
```text
bin/                 실행 launcher
src/                 변환 로직
scripts/             설치/실행/빌드 helper
assets/icons/        PyInstaller 앱 아이콘
tests/               unit tests
.github/workflows/   GitHub Actions release build
```

## 안전 규칙
- 한 번 실행하고 종료합니다. 상주 watcher가 아닙니다.
- 입력 폴더의 root 파일만 스캔합니다. 하위 폴더는 v1에서 무시합니다.
- 숨김 파일과 생성 폴더(`변환/`, `원본완료/`, `logs/`)는 건드리지 않습니다.
- 기존 Markdown이나 이동 대상 원본을 덮어쓰지 않습니다. 충돌 시 `report-001.md`처럼 번호를 붙입니다.
- 변환 성공한 원본만 `원본완료/<형식>/`로 이동합니다.
- 실패한 파일은 원래 위치에 그대로 둡니다.
- URL, cloud, LLM, OCR, audio 변환은 v1 범위가 아닙니다.

## 문제 해결
- `MarkItDown is not installed`: venv를 활성화한 뒤 `python -m pip install -r requirements.txt`를 실행하세요.
- Python 버전 오류: Python 3.10+인지 확인하세요.
- 권한 오류: 입력 폴더와 생성 폴더에 쓰기 권한이 있는지 확인하세요.
- 지원하지 않는 파일: 지원 확장자 목록에 없는 파일은 건너뜁니다.
- 변환 품질 문제: PDF/DOCX/PPTX/XLSX 품질은 MarkItDown과 원본 파일 상태에 좌우됩니다. 중요한 파일은 샘플 검수 후 사용하세요.

## 제한 사항
- recursive scan 없음
- watcher 없음
- Finder/Explorer 자동화 없음
- cloud/LLM/OCR/audio/URL 처리 없음
- macOS notarization/signing 없음
- Windows code signing 없음
- OS별 binary는 해당 OS에서 빌드해야 함

## 향후 개선
- CI에서 OS별 빌드 자동화
- public 배포 전 signing/notarization 검토
- `--onefile` 옵션 검증
- 실제 MarkItDown 설치 환경의 integration smoke test 추가
