"""Print the release notes for VERSION: the body of the top CHANGELOG.md section, which must be headed
`## VERSION`. Fails when the top section is still `## Unreleased` or names another version.

    python3 tools/release_notes.py 0.1.0 > notes.md
"""

import sys

from addon import UNRELEASED, read_changelog


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: release_notes.py VERSION")
    version = sys.argv[1]
    sections = read_changelog()
    if not sections:
        sys.exit("CHANGELOG.md has no ## sections")
    heading, body = sections[0]
    if heading != version:
        hint = "rename it" if heading == UNRELEASED else "fix it"
        sys.exit(f"CHANGELOG.md's top section is '## {heading}', but this release is {version}: "
                 f"{hint} to '## {version}' in a PR first")
    if not body:
        sys.exit(f"CHANGELOG.md's '## {version}' section is empty")
    print(body)


if __name__ == "__main__":
    main()
