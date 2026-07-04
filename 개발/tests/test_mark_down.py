import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "개발" / "src"
sys.path.insert(0, str(SRC_DIR))

import mark_down


class FakeConverter:
    def __init__(self, fail_names=None):
        self.fail_names = set(fail_names or [])
        self.seen = []

    def convert(self, source: Path) -> str:
        self.seen.append(source.name)
        if source.name in self.fail_names:
            raise RuntimeError("fake conversion failed")
        return f"# converted {source.name}\n"


class MarkDownTests(unittest.TestCase):
    def test_supported_extensions(self):
        for extension in mark_down.SUPPORTED_EXTENSIONS:
            self.assertTrue(mark_down.is_supported_extension(extension))
            self.assertTrue(mark_down.is_supported_extension(f".{extension}"))
        for extension in ["png", "mp3", "", "url"]:
            self.assertFalse(mark_down.is_supported_extension(extension))

    def test_scan_root_only_skips_nested_hidden_and_generated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / "b.pdf").write_text("b", encoding="utf-8")
            (root / "ignore.png").write_text("x", encoding="utf-8")
            (root / ".hidden.txt").write_text("hidden", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "nested.txt").write_text("nested", encoding="utf-8")
            (root / "변환").mkdir()
            (root / "변환" / "old.txt").write_text("old", encoding="utf-8")
            (root / "원본완료").mkdir()
            (root / "원본완료" / "old.txt").write_text("old", encoding="utf-8")

            scanned = [path.name for path in mark_down.scan_root_only(root)]
            self.assertEqual(scanned, ["a.txt", "b.pdf"])

    def test_collision_safe_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "report.md").write_text("old", encoding="utf-8")
            self.assertEqual(mark_down.collision_safe_path(root / "report.md").name, "report-001.md")
            (root / "report-001.md").write_text("old", encoding="utf-8")
            self.assertEqual(mark_down.collision_safe_path(root / "report.md").name, "report-002.md")

    def test_successful_conversion_moves_source_and_writes_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "report.txt"
            source.write_text("hello", encoding="utf-8")

            summary = mark_down.convert_folder(root, converter=FakeConverter())

            self.assertEqual(summary.converted, 1)
            self.assertEqual(summary.moved, 1)
            self.assertFalse(source.exists())
            self.assertEqual(
                (root / "변환" / "txt" / "report.md").read_text(encoding="utf-8"),
                "# converted report.txt\n",
            )
            self.assertTrue((root / "원본완료" / "txt" / "report.txt").exists())
            log_lines = (root / "logs" / "conversions.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(json.loads(log_lines[0])["status"], "converted")

    def test_collision_safe_move_and_markdown_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "report.txt"
            source.write_text("new", encoding="utf-8")
            (root / "변환" / "txt").mkdir(parents=True)
            (root / "원본완료" / "txt").mkdir(parents=True)
            (root / "변환" / "txt" / "report.md").write_text("old", encoding="utf-8")
            (root / "원본완료" / "txt" / "report.txt").write_text("old", encoding="utf-8")

            summary = mark_down.convert_folder(root, converter=FakeConverter())

            self.assertEqual(summary.converted, 1)
            self.assertTrue((root / "변환" / "txt" / "report-001.md").exists())
            self.assertTrue((root / "원본완료" / "txt" / "report-001.txt").exists())
            self.assertEqual((root / "원본완료" / "txt" / "report.txt").read_text(encoding="utf-8"), "old")

    def test_failed_conversion_keeps_source_and_logs_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "bad.txt"
            source.write_text("hello", encoding="utf-8")

            summary = mark_down.convert_folder(root, converter=FakeConverter(fail_names={"bad.txt"}))

            self.assertEqual(summary.failed, 1)
            self.assertTrue(source.exists())
            self.assertFalse((root / "변환").exists())
            log_lines = (root / "logs" / "conversions.jsonl").read_text(encoding="utf-8").splitlines()
            event = json.loads(log_lines[0])
            self.assertEqual(event["status"], "failed")
            self.assertIn("fake conversion failed", event["error"])

    def test_failed_move_removes_markdown_and_keeps_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "report.txt"
            source.write_text("hello", encoding="utf-8")
            original_move = mark_down.move_file_no_overwrite

            def fail_move(source_path: Path, destination_path: Path) -> None:
                raise PermissionError("move blocked")

            try:
                mark_down.move_file_no_overwrite = fail_move
                summary = mark_down.convert_folder(root, converter=FakeConverter())
            finally:
                mark_down.move_file_no_overwrite = original_move

            self.assertEqual(summary.failed, 1)
            self.assertTrue(source.exists())
            self.assertFalse((root / "변환" / "txt" / "report.md").exists())
            self.assertFalse((root / "원본완료" / "txt" / "report.txt").exists())
            log_lines = (root / "logs" / "conversions.jsonl").read_text(encoding="utf-8").splitlines()
            event = json.loads(log_lines[0])
            self.assertEqual(event["status"], "failed")
            self.assertIn("move blocked", event["error"])

    def test_dry_run_does_not_write_move_or_convert(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "report.txt"
            source.write_text("hello", encoding="utf-8")
            converter = FakeConverter()

            summary = mark_down.convert_folder(root, converter=converter, dry_run=True)

            self.assertEqual(summary.planned, 1)
            self.assertEqual(converter.seen, [])
            self.assertTrue(source.exists())
            self.assertFalse((root / "변환").exists())
            self.assertFalse((root / "원본완료").exists())
            self.assertFalse((root / "logs").exists())

    def test_source_mode_cli_smoke_with_list_supported(self):
        completed = subprocess.run(
            [sys.executable, "실행/mark_down.py", "--list-supported"],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("txt", completed.stdout.splitlines())

    def test_cli_requires_input_for_conversion(self):
        completed = subprocess.run(
            [sys.executable, "실행/mark_down.py"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("--input is required", completed.stderr)

    def test_readme_contract(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        required = [
            "## 만든 목적",
            "## 지원 파일",
            "## macOS 설치",
            "## macOS 실행",
            "## Windows 설치",
            "## Windows 실행",
            "## 안전 규칙",
            "Python 3.10+",
            "## repo 구조",
            "변환/<형식>/",
            "원본완료/<형식>/",
            "Microsoft MarkItDown",
            "실행/",
            "개발/",
            "--input",
            "--dry-run",
        ]
        for text in required:
            self.assertIn(text, readme)
        for text in ["PyInstaller", "pyinstaller", "requirements-dev", "assets/icons"]:
            self.assertNotIn(text, readme)


if __name__ == "__main__":
    unittest.main()
