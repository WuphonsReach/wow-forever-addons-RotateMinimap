# Changelog

Add new entries under `## Unreleased` at the top. To release, rename that heading to the next version in a PR. `python3 tools/next_version.py` prints the next version, and CI prints it too. The merge publishes the release, with that section as the release notes. See [docs/publishing.md](docs/publishing.md).

## 0.1.2

- The addon now has an icon in the AddOn List: a compass face with the player arrow pointing up and the N turned away from the top.

## 0.1.1

- Fix: the minimap stayed fixed with north at the top after a character switch, until the next loading screen. The client resets the setting after the addon sets it at login, so the addon now sets it again when the client changes it.

## 0.1.0

- First release. Switches the game's `rotateMinimap` setting on at login and after every loading screen, so the minimap turns with your facing. The Forever client drops the setting at login, so `/console rotateMinimap 1` alone doesn't last.
