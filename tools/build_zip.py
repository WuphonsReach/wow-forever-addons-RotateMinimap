"""Build the release zip: dist/RotateMinimap-<version>.zip with the RotateMinimap/ folder at its top level,
holding the .toc (with @project-version@ replaced by the version), the files it lists, LICENSE and CHANGELOG.md.

    python3 tools/build_zip.py 0.1.0
"""

import re
import sys
import zipfile

from addon import ADDON, ROOT, TOC, VERSION_TOKEN, read_toc

FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # same bytes for the same content, whenever it is built


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.]+)?", sys.argv[1]):
        sys.exit("usage: build_zip.py MAJOR.MINOR.PATCH[-SUFFIX]")
    version = sys.argv[1]
    _, files = read_toc()

    toc_text = TOC.read_text(encoding="utf-8")
    if VERSION_TOKEN not in toc_text:
        sys.exit(f"{TOC.name} has no {VERSION_TOKEN} to fill in")
    entries = {TOC.name: toc_text.replace(VERSION_TOKEN, version).encode("utf-8")}
    for name in files + ["LICENSE", "CHANGELOG.md"]:
        entries[name] = (ROOT / name).read_bytes()

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"{ADDON}-{version}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            info = zipfile.ZipInfo(f"{ADDON}/{name}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
