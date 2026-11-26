"""Print the next release version: major and minor from version.yml, patch one past the highest
existing tag v<major>.<minor>.N (0 if there is none). Needs the tags fetched (fetch-depth: 0 in CI)."""

from addon import next_version

if __name__ == "__main__":
    print(next_version())
