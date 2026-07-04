# Mark Down 폴더 정리 도구

빠른 따라하기는 [사용방법.md](/Users/donghoon/Desktop/Work_W_Claude/mark_down/사용방법.md)를 먼저 보면 됩니다.

## 만든 목적
로컬 폴더에 모인 문서 파일을 Microsoft MarkItDown 기반으로 Markdown으로 변환하고, 원본 파일을 형식별로 따로 보관하기 위한 도구입니다.

## 한 줄 요약
`실행/mark_down.py --input <정리할 폴더>`를 실행하면 Markdown 결과는 `변환/<형식>/`에 저장되고, 성공한 원본은 `원본완료/<형식>/`로 이동합니다.

## 빠른 시작
GitHub에서 ZIP으로 내려받거나 clone한 뒤 실행합니다.

```bash
git clone https://github.com/daneyoh/markitdown_folder.git
cd markitdown_folder
```

macOS:

```bash
실행/macOS/setup.command
실행/macOS/open_gui.command
```

Windows PowerShell:

```powershell
.\실행\Windows\setup.ps1
.\실행\Windows\open_gui.bat
```

설치가 끝나면 repo 안에 `변환할PDF/` 폴더도 자동으로 만들어집니다.

가장 쉬운 사용법은 문서를 `변환할PDF/`에 넣고 실행 파일만 여는 것입니다. 실행 직후 그 폴더를 자동 변환합니다.

`open_gui.command` 또는 `open_gui.bat`는 GUI 없이 `변환할PDF/` 안의 파일을 바로 변환합니다. 다른 위치의 파일을 직접 고르는 GUI가 필요하면 `실행/mark_down_gui.py`를 별도로 실행할 수 있습니다.

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
python3 실행/mark_down.py --list-supported
```

## 폴더 구조
예를 들어 `/Users/you/Desktop/work-folder/report.pdf`를 변환하면:

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

`변환/<형식>/`에는 Markdown 결과물만 들어갑니다. 원본 파일은 `원본완료/<형식>/`에 따로 보관합니다.

## macOS 설치
Python 3.10+ 환경에서 실행하세요.

```bash
cd markitdown_folder
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r 개발/requirements.txt
```

또는:

```bash
실행/macOS/setup.command
```

Finder에서 더블클릭할 때는 `실행/macOS/setup.command`를 쓰면 Terminal로 바로 실행됩니다.

`실행/macOS/setup.sh`는 내부 실제 스크립트이고, `실행/macOS/setup.command`가 이것을 호출합니다.
설치가 끝나면 `변환할PDF/` 폴더가 자동 생성됩니다.

## macOS 실행
가장 쉬운 방법은 `변환할PDF/`에 파일을 넣고 아래 실행 파일을 더블클릭하는 것입니다. 실행 직후 자동 변환됩니다. GUI 창이나 파일 선택은 필요 없습니다.

터미널 없이 실행:

```bash
실행/macOS/open_gui.command
```

자동 변환 대신 다른 파일을 직접 고르려면 `python 실행/mark_down_gui.py`로 GUI를 열고 `파일 선택`을 누르세요.

단, `변환할PDF/`에 파일이 있으면 GUI를 열자마자 자동 변환이 시작됩니다. dry-run으로 먼저 확인하려면 `변환할PDF/`를 비운 채 GUI를 열고, `dry-run 먼저 보기`를 켠 뒤 파일을 선택하고 `변환 시작`을 누르세요.

터미널로 폴더 단위 변환도 가능합니다:

```bash
실행/macOS/run.sh --input /Users/you/Desktop/sample-folder
```

미리보기:

```bash
실행/macOS/run.sh --input /Users/you/Desktop/sample-folder --dry-run
```

## Windows 설치
Python 3.10+ 환경에서 실행하세요.

```powershell
cd C:\Users\you\Desktop\markitdown_folder
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\개발\requirements.txt
```

또는:

```powershell
.\실행\Windows\setup.ps1
```

`.\실행\Windows\setup.ps1`는 `py -3`가 Python 3.10+인지 확인한 뒤 venv를 만듭니다.
설치가 끝나면 `변환할PDF\` 폴더가 자동 생성됩니다.

## Windows 실행
가장 쉬운 방법은 `변환할PDF\`에 파일을 넣고 아래 실행 파일을 더블클릭하는 것입니다. 실행 직후 자동 변환됩니다. GUI 창이나 파일 선택은 필요 없습니다.

터미널 없이 실행:

```bat
실행\Windows\open_gui.bat
```

자동 변환 대신 다른 파일을 직접 고르려면 `python 실행\mark_down_gui.py`로 GUI를 열고 `파일 선택`을 누르세요.

단, `변환할PDF\`에 파일이 있으면 GUI를 열자마자 자동 변환이 시작됩니다. dry-run으로 먼저 확인하려면 `변환할PDF\`를 비운 채 GUI를 열고, `dry-run 먼저 보기`를 켠 뒤 파일을 선택하고 `변환 시작`을 누르세요.

터미널로 폴더 단위 변환도 가능합니다:

```bat
실행\Windows\run.bat --input C:\Users\you\Desktop\sample-folder
```

미리보기:

```bat
실행\Windows\run.bat --input C:\Users\you\Desktop\sample-folder --dry-run
```

## 옵션
- `--input`: 한 번 스캔할 로컬 폴더입니다. 필수입니다.
- `--output`: Markdown 출력 폴더입니다. 기본값은 `변환`입니다.
- `--processed`: 성공한 원본 이동 폴더입니다. 기본값은 `원본완료`입니다.
- `--log`: JSONL 로그 파일입니다. 기본값은 `logs/conversions.jsonl`입니다.
- `--dry-run`: 쓰기와 이동 없이 예정 작업만 출력합니다.
- `--list-supported`: 지원 확장자를 출력합니다.

## repo 구조
```text
README.md            사용 설명
실행/mark_down.py    공통 Python launcher
실행/auto_convert.py 기본 폴더 자동 변환 launcher
실행/mark_down_gui.py 파일 선택 GUI launcher
실행/test_board.py   로컬 테스트보드 생성/검증
실행/macOS/          macOS용 설치/실행 스크립트
실행/Windows/        Windows용 설치/실행 스크립트
개발/src/            변환 로직
개발/tests/          unit tests
개발/requirements.txt  Microsoft MarkItDown 의존성
.github/workflows/   CI 테스트
```

## 배포 정책
v1은 `.exe`나 `.app`을 배포하지 않습니다. 서명되지 않은 실행파일은 Windows SmartScreen이나 macOS Gatekeeper 경고를 만들 수 있어서, v1은 Python 설치형으로만 제공합니다.

아이콘 변경도 v1 범위가 아닙니다. 순수 Python 파일의 아이콘은 사용자 OS의 파일 연결 설정에 묶여 있어 repo에서 일관되게 보장하기 어렵습니다.

## 안전 규칙
- 한 번 실행하고 종료합니다. 상주 watcher가 아닙니다.
- `open_gui.command`와 `open_gui.bat`는 `변환할PDF/` 폴더를 바로 자동 변환합니다.
- GUI에서 파일을 직접 선택할 수도 있습니다. 선택한 각 파일의 원본 폴더 기준으로 결과 폴더가 생성됩니다.
- `변환할PDF/README.txt`는 기본 안내 파일로 보고 자동 변환 대상에서 제외합니다.
- `--input`으로 지정한 폴더의 root 파일만 스캔합니다. 하위 폴더는 v1에서 무시합니다.
- 숨김 파일과 생성 폴더(`변환/`, `원본완료/`, `logs/`)는 건드리지 않습니다.
- 기존 Markdown이나 이동 대상 원본을 덮어쓰지 않습니다. 충돌 시 `report-001.md`처럼 번호를 붙입니다.
- 변환 성공한 원본만 `원본완료/<형식>/`로 이동합니다.
- 실패한 파일은 원래 위치에 그대로 둡니다.
- URL, cloud, LLM, OCR, audio 변환은 v1 범위가 아닙니다.

## 문제 해결
- `MarkItDown is not installed`: venv를 활성화한 뒤 `python -m pip install -r 개발/requirements.txt`를 실행하세요.
- Python 버전 오류: Python 3.10+인지 확인하세요.
- 권한 오류: 입력 폴더와 생성 폴더에 쓰기 권한이 있는지 확인하세요.
- 지원하지 않는 파일: 지원 확장자 목록에 없는 파일은 건너뜁니다.
- 변환 품질 문제: PDF/DOCX/PPTX/XLSX 품질은 Microsoft MarkItDown과 원본 파일 상태에 좌우됩니다. 중요한 파일은 샘플 검수 후 사용하세요.

## 제한 사항
- recursive scan 없음
- watcher 없음
- Finder/Explorer 자동화 없음
- cloud/LLM/OCR/audio/URL 처리 없음
- `.exe` / `.app` 배포 없음
- 아이콘 보장 없음

## 향후 개선
- 서명된 앱/실행파일 배포 검토
- 실제 Microsoft MarkItDown 설치 환경의 integration smoke test 추가

## 만든 사람
[@GAZUA_KOR](https://x.com/GAZUA_KOR) — 팔로우 환영합니다!
