"""Decide whether main is ready to release: print `due`, `version` and `reason` as key=value lines
(for $GITHUB_OUTPUT), and the reason on stderr for the log.

A release is due when CHANGELOG.md's top section is headed with the next version (next_version.py),
which by construction has no tag yet. `## Unreleased`, or the version already released, means not due.
"""

import sys

from addon import UNRELEASED, next_version, read_changelog


def main():
    upcoming = next_version()
    sections = read_changelog()
    top = sections[0][0] if sections else None
    due = top == upcoming
    if due:
        reason = f"CHANGELOG.md's top section is '## {upcoming}', which has no tag yet"
    elif top == UNRELEASED:
        reason = f"CHANGELOG.md's top section is '## {UNRELEASED}'"
    elif top is None:
        reason = "CHANGELOG.md has no ## sections"
    else:
        reason = (f"CHANGELOG.md's top section is '## {top}', not the next version {upcoming} "
                  "(already released, or version.yml not bumped)")
    print(f"due={'true' if due else 'false'}")
    print(f"version={upcoming}")
    print(f"reason={reason}")
    print(("Release due: " if due else "No release: ") + reason, file=sys.stderr)


if __name__ == "__main__":
    main()
