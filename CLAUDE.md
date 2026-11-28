# CLAUDE.md

This file gives guidance to Claude Code (claude.ai/code) for work in this repository.

## What this is

A one-file addon for WoW Forever (client 1.60.1, `## Interface: 16001`). It keeps the game's `rotateMinimap` setting (a console variable, or CVar) on. The Forever client resets the setting to 0 just after `VARIABLES_LOADED`, at every login, character switch and `/reload`. Loading screens don't reset it. The description for players is in [README.md](README.md).

- The display name is Rotate Minimap (Forever). It is the `.toc` `## Title`, the README heading, and the CurseForge project title in the future.
- The folder, the `.toc` file and the code keep the name `RotateMinimap`.
- The addon supports only Forever, on purpose. Other WoW versions have a "Rotate Minimap" checkbox in their options, and Forever has none. Do not add `.toc` files for other versions.

The repo is public on GitHub ([WuphonsReach/wow-forever-addons-RotateMinimap](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap), MIT).

- Releases go to GitHub only, not to CurseForge yet. A merged release PR publishes a release ([docs/publishing.md](docs/publishing.md)).
- There is no build step and there are no unit tests. The client loads the `.lua` and `.toc` files as they are.
- The user does all in-game tests.

## Layout

The addon's files are at the repo root, which is usual for a small repo with one addon. The repo root is the addon folder, so the installed folder must have the name `RotateMinimap` to match the `.toc`.

- [RotateMinimap.toc](RotateMinimap.toc): the metadata and the file list.
  - `## Interface: 16001` is Forever 1.60.1. When the client's interface number changes, update it here. If you do not, the addon shows as out of date.
  - `## Version` stays `@project-version@` in the repo. The release build writes the real number. This is the token of the BigWigs packager, so the packager can replace the build later with no changes.
- [RotateMinimap.lua](RotateMinimap.lua): one frame listens for `PLAYER_LOGIN`, `VARIABLES_LOADED` and `CVAR_UPDATE` (for `rotateMinimap` only). It calls `SetCVar("rotateMinimap", ROTATE)` only when the value is different. It uses no SavedVariables and has no options UI. `ROTATE` is the only setting.
  - `CVAR_UPDATE` does the real work. `VARIABLES_LOADED`, and the reset after it, can come after `PLAYER_LOGIN` and `PLAYER_ENTERING_WORLD`, for example after a character switch.
  - The addon sets changes back only until `GUARD` seconds (10) after `VARIABLES_LOADED`. A later change comes from the player, for example `/console rotateMinimap 0` or a Rotate Minimap option in a future client, and the addon keeps it until the next login or `/reload`. Do not make the addon fight the player's choice.
  - Loading screens don't reset the setting, so the addon does nothing at `PLAYER_ENTERING_WORLD`.
  - To find out when the client changes a setting, use the debug branch (see "Debug branch" below).
- [icon.tga](icon.tga): the icon in the AddOn List. `## IconTexture` in the `.toc` names it.
  - It is a 64×64, 32-bit, uncompressed TGA with the rows stored from the bottom, as the other Forever addons use.
  - Do not edit the icon files by hand. Change [make_icon.py](tools/make_icon.py), then run `python3 tools/make_icon.py --render`. This needs `rsvg-convert` and ImageMagick 7 (`magick`).
- `media/`: the icon files that `make_icon.py` writes, and the README pictures. They are not in the release zip.
  - [minimap-before-after.png](media/minimap-before-after.png): the before and after picture in the README, two crops with a bronze divider between them. The crops come from the top-right corner of the user's in-game screenshots: the minimap, the zone name and the clock. They show no chat and no player names. A new picture from a screenshot must leave those out too.
  - [icon.svg](media/icon.svg): the source of `icon.tga`.
  - [icon-curseforge.svg](media/icon-curseforge.svg) and [icon-curseforge-400.png](media/icon-curseforge-400.png): the detailed version, for the CurseForge project avatar and the README.
  - The N is a letter from the Grenze typeface (SIL Open Font License), stored in `make_icon.py` as a path. The SVGs need no font file.
  - [concepts/](media/concepts/README.md): the scripts that drew the earlier icon options. They are for reference only.
- [version.yml](version.yml): the major and minor version of the next release. It has only `major: N` and `minor: N` lines.
- [CHANGELOG.md](CHANGELOG.md): one `## <version>` section for each release, newest first. A `## Unreleased` section at the top holds changes that are not released yet. Every PR that changes the addon adds a line to it.
- `tools/`: Python scripts that need no Python packages. Only `make_icon.py --render` needs other programs.
  - [check_repo.py](tools/check_repo.py) checks `version.yml`, the `.toc` (and its icon file) and the CHANGELOG headings.
  - [next_version.py](tools/next_version.py) prints the next version.
  - [release_notes.py](tools/release_notes.py) prints the top CHANGELOG section for a version.
  - [release_due.py](tools/release_due.py) tells if a release is due.
  - [build_zip.py](tools/build_zip.py) builds `dist/RotateMinimap-<version>.zip`.
  - [make_icon.py](tools/make_icon.py) draws the icon SVGs. With `--render`, it also writes `icon.tga` and the CurseForge PNG.
  - [addon.py](tools/addon.py) holds the helpers that the other scripts share.
- `local/`: a folder for local files, for example notes, logs and screenshots. Git ignores it, and luacheck skips it. Put files here that must not go into the public repo.
  - `local/evidence/YYYY-MM-DD/` holds the redacted screenshots of a test day, a copy of the debug log, and a `README.md` that says what each shot shows.

If the addon needs more than one folder in the future (a second addon, or folders for development only), do these steps:

1. Move the addon to `RotateMinimap/RotateMinimap.toc`.
2. Update `tools/addon.py`.
3. Use `.pkgmeta` `move-folders`, as Forever repos with more than one addon do.

## Checks

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
luacheck .                          # lint; .luacheckrc lists every WoW global the addon may read
python3 tools/check_repo.py         # version.yml parses; the .toc has its fields and lists every root .lua file; CHANGELOG headings in order
python3 tools/next_version.py       # the version the next release would get
python3 tools/build_zip.py 0.0.0-test && unzip -l dist/RotateMinimap-0.0.0-test.zip
```

When the addon starts to use a new WoW global, add it to `read_globals` in [.luacheckrc](.luacheckrc). If you do not, luacheck fails.

## CI

[.github/workflows/checks.yml](.github/workflows/checks.yml) runs on every PR and every push to `main`. It has two jobs:

- `luacheck`.
- `repo-checks`: compiles `tools/`, runs `check_repo.py` and `next_version.py`, and builds a test zip.

The job names are the status checks that the `pr-checks` ruleset requires. If you rename a job, update the ruleset in the same change. If you do not, every PR waits for a check that never reports.

The workflows pin actions to full commit SHAs, with the version in a trailing comment, as in the TF3 repos. To find the SHA, run `gh api repos/<owner>/<action>/git/ref/tags/<tag>`.

## Releasing

The steps for people are in [docs/publishing.md](docs/publishing.md). When the workflow changes, change that file too.

A merged release PR publishes the release, and nothing else does. A release PR renames the top `## Unreleased` heading of CHANGELOG.md to the next version.

[.github/workflows/release.yml](.github/workflows/release.yml) runs on every push to `main`. You can also start it manually, as a fallback. It has three jobs:

- `decide` runs [release_due.py](tools/release_due.py).
  - A release is due when the top CHANGELOG heading is the same as the output of `next_version.py`. That is `major.minor` from `version.yml`, plus a patch number one more than the highest `v<major>.<minor>.N` tag, or 0.
  - If no release is due, a push finishes green with a notice, and a manual run fails.
  - The job also fails when it starts from a branch other than `main`.
- `checks` calls `checks.yml`.
- `release` makes sure that the version is still free. It takes the notes from that CHANGELOG section (`release_notes.py`) and builds the zip. Then it creates the tag `v<version>` and the GitHub release together, on the pushed commit.

Safeguards:

- `check_repo.py` accepts only these top headings:
  - `Unreleased`.
  - The next version.
  - The latest tag (just released).
- `check_repo.py` also fails when the text of a released section is different from its text at its tag.
- Thus a wrong number, or an entry under an old version, fails on the PR. A PR with a wrong number cannot start a release by accident.
- Nobody can change a tag (`version-tags` ruleset) or a release (the immutable releases setting of the repo) after it is published. To correct a bad release, publish a new version.
- The release zip has the `RotateMinimap/` folder at its top level. A wrapper folder around it stops the addon from loading. The folder holds:
  - The `.toc`.
  - The files that the `.toc` lists.
  - The `## IconTexture` file (`icon.tga`).
  - `LICENSE`.
  - `CHANGELOG.md`.

A move to CurseForge is planned (BigWigs packager v2.7.0 or later, the `CF_API_TOKEN` secret, `## X-Curse-Project-ID`). The steps are in docs/publishing.md, "CurseForge, later".

## Testing in game

The steps for people are in [docs/development.md](docs/development.md). Keep that file in step with this section.

- In the user's game install, `_forever_/Interface/AddOns/RotateMinimap` is a link to the repo root. The game loads the files of the checked-out branch, so there is no copy step after a change.
- A change to the `.lua` file shows after `/reload`. A change to the `.toc` needs a full restart.
- To check: the addon shows in the AddOn List at character select, with "Load out of date AddOns" cleared. After login, the minimap rotates with no `/console rotateMinimap 1`. After `/console rotateMinimap 0`, it stays north-up until the next login or `/reload`.
- Files from the repo show `@project-version@` as their version. This is harmless.

### Debug branch

The user tests on a local branch with debug logging, for example `2026-11-26-debug-logging`. It is `main` plus `DEBUG` lines in three files:

- `RotateMinimap.lua` logs each event and the value of `rotateMinimap` to chat and to the saved variable `RotateMinimapDebugLog`. After each change of the value, it reads the value again 5 seconds later.
- `RotateMinimap.toc` adds `## SavedVariables: RotateMinimapDebugLog`.
- `.luacheckrc` adds the globals that the logging uses.

Rules for the debug branch:

- Keep it up to date: merge `origin/main` into it. Resolve conflicts so that the logging wraps the logic of `main`, with no other changes.
- Never push it, and never open a PR from it. Make fixes on a new branch from `origin/main`, without the `DEBUG` lines.
- After work on another branch, check out the debug branch again, because the game loads the checked-out branch. To edit a branch from `main` without a change of checkout, use a worktree in `local/`.
- The client writes the saved variable to `_forever_/WTF/Account/<account>/SavedVariables/RotateMinimap.lua` only at logout, `/reload` or exit. Chat shows the current session. Do not write to `WTF/` while the game runs.
- Screenshots show character names and the names of other players. Do not put them, or details from them, in committed files.

Screenshots of debug output (the user's shots are at the top of `~/Pictures/Screenshots/`):

1. Find the shots that show the green `RotateMinimap` prefix (colour `33ff99`) in chat.
2. Redact each one: keep only the debug lines in chat, with their wrapped lines, and the minimap, which shows whether the map turns. Make everything else black. A 4K shot drops from about 5 MB to about 300 KB.
3. Look at every redacted shot before you replace an original. Keep the originals in a temporary backup until the user is satisfied.
4. Move the redacted shots into `local/evidence/YYYY-MM-DD/`. Add a `README.md` that says, for each shot or group, what was tested and what it shows, and put a copy of the debug log next to it.

## Repo rules

The rulesets match the user's TF3 mod repos. They have no bypass actors, so they apply to the owner too.

- `main`: changes go to `main` only through a pull request (0 approvals necessary).
- `pr-checks`: PRs into the default branch need the `luacheck` and `repo-checks` status checks to pass.
- `trunks`: nobody can delete or force-push `main`.
- `version-tags`: nobody can move or delete a tag that matches `v*.*` after it is pushed.

Make branches from `origin/main`, named `<YYYY-MM-DD>-<slug>`. Commit, push or open a PR only when the user asks.

## Public repo

This repo is public. Keep these out of committed files:

- Game account names, character names, and realm or server ids.
- Home paths and machine details.

The GitHub owner name (WuphonsReach) is public and is permitted, for example as the `.toc` author. Write game paths from `_forever_/`.
