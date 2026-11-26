# Changelog

New entries go under `## Unreleased` at the top. To release, rename that heading to the version the release will get (`python3 tools/next_version.py`, also printed by CI); the release workflow uses that section as the release notes.

## 0.1.0

- First release. Switches the game's `rotateMinimap` setting on at login and after every loading screen, so the minimap turns with your facing. The Forever client drops the setting at login, so `/console rotateMinimap 1` alone doesn't last.
