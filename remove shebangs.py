# coding=utf-8
from pathlib import Path

ROOT: Path = Path("/home/stsav012/Projects/pyHM/advantech_daq")

fn: Path
for fn in ROOT.iterdir():
    if not fn.is_file():
        continue

    text: str = fn.read_text()
    if not text.startswith("#!"):
        continue

    lines: list[str] = text.splitlines(keepends=True)
    while lines[0].startswith("#!"):
        lines.pop(0)

    fn.write_text("".join(lines))
