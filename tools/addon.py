"""Shared helpers for the repo tools: read version.yml and the .toc file."""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADDON = "RotateMinimap"
TOC = ROOT / f"{ADDON}.toc"
VERSION_FILE = ROOT / "version.yml"
CHANGELOG = ROOT / "CHANGELOG.md"
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


VERSION_RE = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
UNRELEASED = "Unreleased"


def version_tags():
    """Return the existing release tags as (major, minor, patch) tuples."""
    out = subprocess.run(
        ["git", "tag", "--list", "v*"], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.split()
    return [tuple(int(g) for g in m.groups()) for t in out if (m := re.fullmatch("v" + VERSION_RE, t))]


def next_version():
    """major.minor from version.yml, patch one past the highest tag v<major>.<minor>.N (0 if none)."""
    major, minor = read_version_file()
    patches = [p for (a, b, p) in version_tags() if (a, b) == (major, minor)]
    return f"{major}.{minor}.{max(patches) + 1 if patches else 0}"


def changelog_at_tag(version):
    """CHANGELOG.md's text as of tag v<version>, or None if the tag or the file there doesn't exist."""
    r = subprocess.run(["git", "show", f"v{version}:CHANGELOG.md"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def read_changelog(text=None):
    """Return the CHANGELOG.md sections (or those of `text`) as a list of (heading, body), in file order."""
    if text is None:
        text = CHANGELOG.read_text(encoding="utf-8")
    sections = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if line.startswith("## ") and not in_fence:
            sections.append((line[3:].strip(), []))
        elif sections:
            sections[-1][1].append(line)
    return [(h, "\n".join(body).strip()) for h, body in sections]


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
