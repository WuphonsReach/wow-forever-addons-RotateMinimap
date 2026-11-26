"""Shared helpers for the repo tools: read version.yml and the .toc file."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADDON = "RotateMinimap"
TOC = ROOT / f"{ADDON}.toc"
VERSION_FILE = ROOT / "version.yml"
VERSION_TOKEN = "@project-version@"


def read_version_file():
    """Return (major, minor) from version.yml. Only `key: <integer>` lines are allowed."""
    values = {}
    for n, line in enumerate(VERSION_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.fullmatch(r"(major|minor):\s*(0|[1-9][0-9]*)", line)
        if not m:
            raise ValueError(f"version.yml line {n}: expected 'major: N' or 'minor: N', got {line!r}")
        if m.group(1) in values:
            raise ValueError(f"version.yml line {n}: {m.group(1)} given twice")
        values[m.group(1)] = int(m.group(2))
    missing = {"major", "minor"} - values.keys()
    if missing:
        raise ValueError(f"version.yml: missing {', '.join(sorted(missing))}")
    return values["major"], values["minor"]


def read_toc():
    """Return (fields, files): the `## Key: value` fields and the listed file names, in order."""
    fields, files = {}, []
    for line in TOC.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("##"):
            key, _, value = line[2:].partition(":")
            fields[key.strip()] = value.strip()
        elif line and not line.startswith("#"):
            files.append(line.replace("\\", "/"))
    return fields, files
