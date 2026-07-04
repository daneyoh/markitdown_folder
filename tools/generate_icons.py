#!/usr/bin/env python3
"""Generate simple app icons without external dependencies."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT_DIR / "assets" / "icons"

LETTER_BITMAPS = {
    "M": [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001",
    ],
    "D": [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ],
}


def lerp(start: int, end: int, amount: float) -> int:
    return round(start + (end - start) * amount)


def draw_rect(pixels: bytearray, size: int, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int, int]) -> None:
    x0 = max(0, min(size, x0))
    x1 = max(0, min(size, x1))
    y0 = max(0, min(size, y0))
    y1 = max(0, min(size, y1))
    for y in range(y0, y1):
        for x in range(x0, x1):
            index = (y * size + x) * 4
            pixels[index : index + 4] = bytes(color)


def draw_letter(pixels: bytearray, size: int, letter: str, origin_x: int, origin_y: int, scale: int) -> None:
    color = (255, 255, 255, 255)
    for row, line in enumerate(LETTER_BITMAPS[letter]):
        for col, bit in enumerate(line):
            if bit == "1":
                draw_rect(
                    pixels,
                    size,
                    origin_x + col * scale,
                    origin_y + row * scale,
                    origin_x + (col + 1) * scale,
                    origin_y + (row + 1) * scale,
                    color,
                )


def make_png_bytes(size: int) -> bytes:
    pixels = bytearray(size * size * 4)
    for y in range(size):
        for x in range(size):
            fx = x / max(1, size - 1)
            fy = y / max(1, size - 1)
            red = lerp(44, 18, fy)
            green = lerp(116, 176, fx)
            blue = lerp(255, 170, (fx + fy) / 2)
            alpha = 255
            index = (y * size + x) * 4
            pixels[index : index + 4] = bytes((red, green, blue, alpha))

    margin = size // 7
    card_color = (255, 255, 255, 28)
    draw_rect(pixels, size, margin, margin, size - margin, size - margin, card_color)

    scale = max(1, size // 16)
    letter_height = 7 * scale
    letter_width = 5 * scale
    gap = scale * 2
    total_width = letter_width * 2 + gap
    origin_x = (size - total_width) // 2
    origin_y = (size - letter_height) // 2
    draw_letter(pixels, size, "M", origin_x, origin_y, scale)
    draw_letter(pixels, size, "D", origin_x + letter_width + gap, origin_y, scale)

    raw = bytearray()
    stride = size * 4
    for y in range(size):
        raw.append(0)
        raw.extend(pixels[y * stride : (y + 1) * stride])

    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def write_ico(path: Path, png_images: list[tuple[int, bytes]]) -> None:
    entries = []
    data_offset = 6 + len(png_images) * 16
    payloads = []
    for size, png in png_images:
        width = 0 if size >= 256 else size
        height = 0 if size >= 256 else size
        entries.append(struct.pack("<BBBBHHII", width, height, 0, 0, 1, 32, len(png), data_offset))
        payloads.append(png)
        data_offset += len(png)

    path.write_bytes(struct.pack("<HHH", 0, 1, len(png_images)) + b"".join(entries) + b"".join(payloads))


def write_icns(path: Path, png_images: list[tuple[int, bytes]]) -> None:
    type_by_size = {
        16: b"icp4",
        32: b"icp5",
        64: b"icp6",
        128: b"ic07",
        256: b"ic08",
        512: b"ic09",
        1024: b"ic10",
    }
    chunks = []
    for size, png in png_images:
        icon_type = type_by_size.get(size)
        if icon_type is None:
            continue
        chunks.append(icon_type + struct.pack(">I", len(png) + 8) + png)
    payload = b"".join(chunks)
    path.write_bytes(b"icns" + struct.pack(">I", len(payload) + 8) + payload)


def write_svg(path: Path) -> None:
    path.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#2c74ff"/>
      <stop offset="1" stop-color="#12b0aa"/>
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" rx="192" fill="url(#bg)"/>
  <rect x="148" y="148" width="728" height="728" rx="72" fill="#ffffff" opacity=".12"/>
  <text x="512" y="594" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="290" font-weight="800" fill="#ffffff">MD</text>
</svg>
""",
        encoding="utf-8",
    )


def main() -> int:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    pngs = [(size, make_png_bytes(size)) for size in sizes]
    (ICON_DIR / "mark-down.png").write_bytes(dict(pngs)[1024])
    write_ico(ICON_DIR / "mark-down.ico", [(size, png) for size, png in pngs if size in {16, 32, 48, 256}])
    write_icns(ICON_DIR / "mark-down.icns", pngs)
    write_svg(ICON_DIR / "mark-down.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
