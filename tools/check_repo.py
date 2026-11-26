"""Repo checks that CI runs on every PR: version.yml parses, the .toc has the fields a release needs,
the files it lists match the .lua files in the repo root, and CHANGELOG.md's headings are in order."""

import re
import sys

from addon import (CHANGELOG, ROOT, TOC, UNRELEASED, VERSION_RE, VERSION_TOKEN, next_version, read_changelog,
                   read_toc, read_version_file, version_tags)


def check_changelog():
    """The top section is `Unreleased`, the next release's version, or the latest tag (just released);
    the rest are released versions, newest first."""
    if not CHANGELOG.is_file():
        return ["CHANGELOG.md is missing"]
    sections = read_changelog()
    if not sections:
        return ["CHANGELOG.md has no ## sections"]
    try:
        upcoming = next_version()
    except ValueError:
        return []  # version.yml is broken; reported above
    tags = sorted(version_tags())
    latest = ".".join(map(str, tags[-1])) if tags else None
    errors = []
    top = sections[0][0]
    allowed = [UNRELEASED, upcoming] + ([latest] if latest else [])
    if top not in allowed:
        errors.append(f"CHANGELOG.md: top section '## {top}' should be one of: "
                      + ", ".join(f"'## {a}'" for a in allowed))
    versions = []
    for i, (heading, body) in enumerate(sections):
        if heading == UNRELEASED and i == 0:
            continue
        if not re.fullmatch(VERSION_RE, heading):
            errors.append(f"CHANGELOG.md: '## {heading}' is not a version (or 'Unreleased' at the top)")
            continue
        if not body:
            errors.append(f"CHANGELOG.md: '## {heading}' is empty")
        versions.append(tuple(int(x) for x in heading.split(".")))
    if versions != sorted(set(versions), reverse=True):
        errors.append("CHANGELOG.md: versions should be unique and newest first")
    return errors


def main():
    errors = []
    try:
        read_version_file()
    except ValueError as e:
        errors.append(str(e))

    fields, files = read_toc()
    for key in ("Interface", "Title", "Author", "Version"):
        if not fields.get(key):
            errors.append(f"{TOC.name}: missing ## {key}")
    if fields.get("Interface") and not fields["Interface"].replace(",", "").replace(" ", "").isdigit():
        errors.append(f"{TOC.name}: ## Interface should be a number, got {fields['Interface']!r}")
    if fields.get("Version") != VERSION_TOKEN:
        errors.append(f"{TOC.name}: ## Version should be {VERSION_TOKEN} (the release build fills it in)")

    for name in files:
        if not (ROOT / name).is_file():
            errors.append(f"{TOC.name} lists {name}, which does not exist")
    for path in sorted(ROOT.glob("*.lua")):
        if path.name != ".luacheckrc" and path.name not in files:
            errors.append(f"{path.name} is not listed in {TOC.name}, so the client won't load it")
    if not (ROOT / "LICENSE").is_file():
        errors.append("LICENSE is missing (it ships in the release zip)")

    errors += check_changelog()

    for e in errors:
        print(f"error: {e}")
    if errors:
        return 1
    print("repo checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
