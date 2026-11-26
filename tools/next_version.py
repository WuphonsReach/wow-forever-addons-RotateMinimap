"""Print the next release version: major and minor from version.yml, patch one past the highest
existing tag v<major>.<minor>.N (0 if there is none). Needs the tags fetched (fetch-depth: 0 in CI)."""

import re
import subprocess
import sys

from addon import ROOT, read_version_file


def main():
    major, minor = read_version_file()
    tags = subprocess.run(
        ["git", "tag", "--list", f"v{major}.{minor}.*"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.split()
    patches = [int(m.group(1)) for t in tags if (m := re.fullmatch(rf"v{major}\.{minor}\.(0|[1-9][0-9]*)", t))]
    patch = max(patches) + 1 if patches else 0
    print(f"{major}.{minor}.{patch}")


if __name__ == "__main__":
    sys.exit(main())
