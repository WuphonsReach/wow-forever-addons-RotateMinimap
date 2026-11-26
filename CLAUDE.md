# CLAUDE.md

This file gives guidance to Claude Code (claude.ai/code) for work in this repository.

## What this is

A one-file addon for WoW Forever (client 1.60.1, `## Interface: 16001`). At login and after every loading screen, it sets the game's `rotateMinimap` setting (a console variable, or CVar) to on. The Forever client drops the setting at login. The description for players is in [README.md](README.md).

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
- [RotateMinimap.lua](RotateMinimap.lua): one frame listens for `PLAYER_LOGIN` and `PLAYER_ENTERING_WORLD`. It calls `SetCVar("rotateMinimap", ROTATE)` only when the value is different. It uses no SavedVariables and has no options UI. `ROTATE` is the only setting.
- [version.yml](version.yml): the major and minor version of the next release. It has only `major: N` and `minor: N` lines.
- [CHANGELOG.md](CHANGELOG.md): one `## <version>` section for each release, newest first. A `## Unreleased` section at the top holds changes that are not released yet. Every PR that changes the addon adds a line to it.
- `tools/`: Python scripts with no dependencies.
  - [check_repo.py](tools/check_repo.py) checks `version.yml`, the `.toc` and the CHANGELOG headings.
  - [next_version.py](tools/next_version.py) prints the next version.
  - [release_notes.py](tools/release_notes.py) prints the top CHANGELOG section for a version.
  - [release_due.py](tools/release_due.py) tells if a release is due.
  - [build_zip.py](tools/build_zip.py) builds `dist/RotateMinimap-<version>.zip`.
  - [addon.py](tools/addon.py) holds the helpers that the other scripts share.

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
  - `LICENSE`.
  - `CHANGELOG.md`.

A move to CurseForge is planned (the BigWigs packager, `CF_API_KEY`, `## X-Curse-Project-ID`). The steps are in docs/publishing.md, "CurseForge, later".

## Testing in game

1. Copy `RotateMinimap.toc` and `RotateMinimap.lua` into `_forever_/Interface/AddOns/RotateMinimap/` in the game install. Or unzip a release zip into `AddOns/`.
2. Fully restart the client if the folder is new. The client finds a new addon folder only after a full restart, not after `/reload`.
3. At character select, make sure that the addon shows in the AddOn List with "Load out of date AddOns" cleared.
4. Log in. Make sure that the minimap rotates with no `/console rotateMinimap 1`.

Notes:

- A copy straight from the repo shows `@project-version@` as its version. This is harmless.
- The installed copy is a plain copy, not a link. Copy it again after every change.
- A change to the `.lua` file shows after `/reload`. A change to the `.toc` needs a full restart.

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
