# Changelog

New entries go under `## Unreleased` at the top. A PR that renames that heading to the next version (`python3 tools/next_version.py`, also printed by CI) publishes the release when merged, with that section as the release notes. See [docs/publishing.md](docs/publishing.md).

## 0.1.0

- First release. Switches the game's `rotateMinimap` setting on at login and after every loading screen, so the minimap turns with your facing. The Forever client drops the setting at login, so `/console rotateMinimap 1` alone doesn't last.
