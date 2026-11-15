"""Renders the Cosmic icon files from cosmic.svg with headless Chrome (or Edge).

Outputs, next to this script:
  cosmic-128.png, cosmic-256.png   window/taskbar icon and update prompt
  cosmic-macos-512.png             Dock icon on Apple's grid (824/1024 body, transparent margin)
  cosmic.ico                       Windows executable icon (16-256 px, PNG-compressed entries)

Run: python -I render_icons.py [path-to-chrome.exe]
"""

import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SVG = HERE / "cosmic.svg"
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]


def browser() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    for b in BROWSERS:
        if Path(b).is_file():
            return b
    raise SystemExit("no Chrome or Edge found; pass the browser path as the first argument")


def render(exe: str, work: Path, size: int, body: int, out: Path) -> None:
    pad = (size - body) / 2
    page = work / f"icon-{size}-{body}.html"
    page.write_text(
        "<html><body style='margin:0;background:transparent'>"
        f"<img src='{SVG.as_uri()}' style='position:absolute;left:{pad}px;top:{pad}px;width:{body}px;height:{body}px'>"
        "</body></html>",
        encoding="utf-8",
    )
    if out.exists():
        out.unlink()
    subprocess.run(
        [
            exe,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--default-background-color=00000000",
            "--allow-file-access-from-files",
            f"--user-data-dir={work / 'profile'}",
            f"--window-size={size},{size}",
            f"--screenshot={out}",
            page.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    if not out.is_file():
        raise SystemExit(f"the browser did not write {out}")
    width, height = struct.unpack(">II", out.read_bytes()[16:24])
    if (width, height) != (size, size):
        raise SystemExit(f"{out.name}: expected {size}x{size}, got {width}x{height}")


def write_ico(pngs: list[tuple[int, bytes]], out: Path) -> None:
    header = struct.pack("<HHH", 0, 1, len(pngs))
    offset = len(header) + 16 * len(pngs)
    entries, data = b"", b""
    for size, png in pngs:
        dim = 0 if size >= 256 else size
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(png), offset + len(data))
        data += png
    out.write_bytes(header + entries + data)


def main() -> None:
    exe = browser()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for size in (128, 256):
            render(exe, work, size, size, HERE / f"cosmic-{size}.png")
        render(exe, work, 512, 412, HERE / "cosmic-macos-512.png")
        pngs = []
        for size in ICO_SIZES:
            target = work / f"ico-{size}.png"
            render(exe, work, size, size, target)
            pngs.append((size, target.read_bytes()))
        write_ico(pngs, HERE / "cosmic.ico")
    print("wrote cosmic-128.png, cosmic-256.png, cosmic-macos-512.png, cosmic.ico")


if __name__ == "__main__":
    main()
