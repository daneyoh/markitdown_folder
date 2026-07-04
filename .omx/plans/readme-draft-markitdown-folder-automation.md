# Mark Down 자동 정리 도구

> 이 문서는 실행 단계에서 루트 `README.md`로 반영할 초안입니다.

## 만든 목적
여러 형식의 문서 파일을 한 폴더에 넣고 명령 한 번으로 Markdown 파일로 바꾸기 위해 만든 도구입니다. 변환된 Markdown은 파일 형식별 폴더로 정리되고, 성공한 원본 파일은 `processed/`로 이동합니다.

## 한 줄 요약
`python mark_down.py`를 실행하면 현재 폴더의 문서 파일을 Markdown으로 변환하고 정리합니다.

## 지원 파일
- PDF: `.pdf`
- Word: `.docx`
- PowerPoint: `.pptx`
- Excel: `.xlsx`
- Web/Text: `.html`, `.txt`, `.csv`, `.json`, `.xml`

## 하지 않는 일
- 폴더를 계속 감시하지 않습니다.
- Finder/Explorer에서 폴더를 여는 순간 자동 실행하지 않습니다.
- 하위 폴더까지 재귀적으로 훑지 않습니다.
- OCR, 오디오 변환, YouTube/URL 변환, LLM/cloud 연동은 v1 범위가 아닙니다.
- 기존 파일을 덮어쓰지 않습니다.

## 결과 폴더 구조
```text
markdown/
  pdf/
  docx/
  pptx/
  xlsx/
processed/
  pdf/
  docx/
logs/
  conversions.jsonl
```

## macOS 설치
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## macOS 실행
```bash
python mark_down.py
```

다른 폴더를 지정하려면:

```bash
python mark_down.py --input /Users/donghoon/Documents/input-folder
```

파일 이동 없이 계획만 보려면:

```bash
python mark_down.py --dry-run
```

또는:

```bash
./scripts/run_macos.sh
```

## Windows 설치
```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Windows 실행
```powershell
python mark_down.py
```

다른 폴더를 지정하려면:

```powershell
python mark_down.py --input C:\Users\DH\Documents\input-folder
```

파일 이동 없이 계획만 보려면:

```powershell
python mark_down.py --dry-run
```

또는:

```bat
scripts\run_windows.bat
```

## 배포용 빌드
macOS 빌드는 macOS에서 실행합니다.

```bash
./scripts/build_macos.sh
```

내부 기준 명령은 다음과 같습니다.

```bash
pyinstaller --onedir --name mark-down mark_down.py
```

Windows 빌드는 Windows에서 실행합니다.

```powershell
.\scripts\build_windows.ps1
```

내부 기준 명령은 다음과 같습니다.

```powershell
pyinstaller --onedir --name mark-down mark_down.py
```

기본 배포 결과는 `dist/mark-down/` 폴더입니다.

`requirements.txt`는 실행용 의존성, `requirements-dev.txt`는 테스트와 PyInstaller 빌드용 의존성을 담습니다.

## 안전 규칙
- 변환 성공 후에만 원본을 `processed/<확장자>/`로 이동합니다.
- 변환 실패 파일은 원래 위치에 그대로 둡니다.
- 같은 이름이 있으면 `-001`, `-002`처럼 번호를 붙입니다.
- 파일 삭제는 하지 않습니다.

## 문제 해결
### `Python 3.10+ required`
MarkItDown은 Python 3.10 이상이 필요합니다. macOS 기본 `python3`가 3.9일 수 있으니 `python3.10` 또는 `python3.12`를 사용하세요.

### `ModuleNotFoundError: markitdown`
가상환경을 활성화한 뒤 `pip install -r requirements.txt`를 실행하세요.

### 변환 실패
실패 파일은 이동하지 않습니다. `logs/conversions.jsonl`에서 실패 이유를 확인하세요.

### macOS에서 실행 차단
공개 배포용 앱은 추후 서명/notarization이 필요할 수 있습니다. v1은 터미널 실행과 로컬 빌드를 기준으로 합니다.

### Windows에서 실행 차단
서명되지 않은 실행 파일은 Windows SmartScreen이나 백신에서 경고가 뜰 수 있습니다. v1은 로컬 빌드와 명령줄 실행을 기준으로 합니다.

## 향후 개선
- 재귀 스캔 옵션
- watch 모드
- `onefile` 배포
- macOS signing/notarization
- Windows code signing
