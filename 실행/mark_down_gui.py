#!/usr/bin/env python3
"""Simple GUI launcher for the Mark Down converter."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "개발" / "src"
sys.path.insert(0, str(SRC_DIR))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from mark_down import Summary, convert_files, convert_folder, scan_root_only  # noqa: E402


def format_summary(summary: Summary, dry_run: bool) -> str:
    lines = [
        (
            "DRY RUN - " if dry_run else ""
        )
        + (
            f"planned={summary.planned} converted={summary.converted} "
            f"skipped={summary.skipped} failed={summary.failed} moved={summary.moved}"
        )
    ]
    for result in summary.results:
        if result.status == "planned":
            lines.append(f"planned: {result.source.name} -> {result.output}")
        elif result.status == "converted":
            lines.append(f"converted: {result.source.name} -> {result.output}")
        elif result.status == "failed":
            lines.append(f"failed: {result.source.name}: {result.error}")
        else:
            lines.append(f"skipped: {result.source.name} ({result.reason})")
    return "\n".join(lines)


class MarkDownGui:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Mark Down File Converter")
        self.root.geometry("760x520")
        self.root.minsize(680, 420)

        self.default_input_dir = ROOT_DIR / "변환할PDF"
        self.selected_files: list[Path] = []
        self.selected_label = tk.StringVar(value="선택된 파일 없음")
        self.dry_run = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="실행하면 변환할PDF 폴더를 먼저 자동 변환합니다.")

        frame = ttk.Frame(root, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

        title = ttk.Label(frame, text="클릭하면 바로 Markdown 변환", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, sticky="w")

        path_row = ttk.Frame(frame)
        path_row.grid(row=1, column=0, sticky="ew", pady=(16, 8))
        path_row.columnconfigure(0, weight=1)

        path_entry = ttk.Entry(path_row, textvariable=self.selected_label, state="readonly")
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        browse_button = ttk.Button(path_row, text="파일 선택", command=self.choose_files)
        browse_button.grid(row=0, column=1)

        controls = ttk.Frame(frame)
        controls.grid(row=2, column=0, sticky="w", pady=(0, 12))

        auto_button = ttk.Button(controls, text="변환할PDF 바로 변환", command=self.run_default_folder)
        auto_button.grid(row=0, column=0, padx=(0, 12))

        dry_run_check = ttk.Checkbutton(controls, text="dry-run 먼저 보기", variable=self.dry_run)
        dry_run_check.grid(row=0, column=1, padx=(0, 12))

        run_button = ttk.Button(controls, text="변환 시작", command=self.run_conversion)
        run_button.grid(row=0, column=2)

        output = tk.Text(frame, wrap="word", height=18)
        output.grid(row=3, column=0, sticky="nsew")
        output.configure(state="disabled")
        self.output = output

        status_label = ttk.Label(frame, textvariable=self.status)
        status_label.grid(row=4, column=0, sticky="w", pady=(12, 0))
        self.root.after(150, self.auto_convert_default_folder)

    def choose_files(self) -> None:
        selected = filedialog.askopenfilenames(
            title="변환할 파일 선택",
            filetypes=[
                ("지원 파일", "*.pdf *.docx *.pptx *.xlsx *.html *.txt *.csv *.json *.xml"),
                ("모든 파일", "*.*"),
            ],
        )
        if selected:
            self.selected_files = [Path(path) for path in selected]
            names = ", ".join(path.name for path in self.selected_files[:3])
            if len(self.selected_files) > 3:
                names += f" 외 {len(self.selected_files) - 3}개"
            self.selected_label.set(names)
            self.status.set("파일을 선택했습니다. 변환 시작을 누르세요.")

    def run_default_folder(self) -> None:
        if not self.default_input_dir.exists():
            messagebox.showerror("기본 폴더 없음", f"기본 폴더가 없습니다: {self.default_input_dir}")
            self.status.set("실패")
            return

        if not scan_root_only(self.default_input_dir):
            self.status.set("변환할PDF 폴더가 비어 있습니다. 파일을 선택하거나 PDF를 넣어 주세요.")
            return

        try:
            summary = convert_folder(self.default_input_dir, dry_run=self.dry_run.get())
        except Exception as exc:
            messagebox.showerror("변환 실패", str(exc))
            self.status.set("실패")
            return

        dry_run = self.dry_run.get()
        self.set_output(format_summary(summary, dry_run=dry_run))
        self.status.set("변환할PDF dry-run 완료" if dry_run else "변환할PDF 변환 완료")
        if not dry_run and summary.failed == 0:
            messagebox.showinfo("완료", f"{self.default_input_dir} 변환이 끝났습니다.")

    def auto_convert_default_folder(self) -> None:
        if self.default_input_dir.exists() and scan_root_only(self.default_input_dir):
            self.run_default_folder()

    def set_output(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def run_conversion(self) -> None:
        if not self.selected_files:
            messagebox.showerror("파일 선택 필요", "먼저 변환할 파일을 선택하세요.")
            return

        try:
            summary = convert_files(self.selected_files, dry_run=self.dry_run.get())
        except Exception as exc:
            messagebox.showerror("변환 실패", str(exc))
            self.status.set("실패")
            return

        dry_run = self.dry_run.get()
        self.set_output(format_summary(summary, dry_run=dry_run))
        self.status.set("dry-run 완료" if dry_run else "변환 완료")
        if not dry_run and summary.failed == 0:
            messagebox.showinfo("완료", "변환이 끝났습니다.")


def main() -> int:
    root = tk.Tk()
    MarkDownGui(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
