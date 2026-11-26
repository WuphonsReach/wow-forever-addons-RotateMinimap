"""Repo checks that CI runs on every PR: version.yml parses, the .toc has the fields a release needs,
and the files it lists match the .lua files in the repo root."""

import sys

from addon import ROOT, TOC, VERSION_TOKEN, read_toc, read_version_file


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

    for e in errors:
        print(f"error: {e}")
    if errors:
        return 1
    print("repo checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
