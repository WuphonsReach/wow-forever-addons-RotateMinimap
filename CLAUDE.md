# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A one-file addon for WoW Forever (client 1.60.1, `## Interface: 16001`). It switches the game's `rotateMinimap` setting (a console variable, or CVar) on at login and after every loading screen, because the Forever client drops the setting at login. The player-facing description is [README.md](README.md).

The display name is **Rotate Minimap (Forever)**: the `.toc` `## Title`, the README heading, and the CurseForge project title when it goes there. The folder, `.toc` file and code keep `RotateMinimap`. Only Forever is supported, on purpose: other WoW versions have a "Rotate Minimap" checkbox in their options, and Forever has none. Don't add `.toc` files for other versions.

The repo is public on GitHub ([WuphonsReach/wow-forever-addons-RotateMinimap](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap), MIT). Releases are published on GitHub only, not on CurseForge yet; merging a release PR publishes one ([docs/publishing.md](docs/publishing.md)). There is no build step and no unit tests. The client loads the `.lua` and `.toc` files as they are, and the user does every in-game test.

## Layout

The addon's files sit at the repo root, which is the usual layout for a small single-addon repo. The repo root is the addon folder, so the installed folder must be named `RotateMinimap` to match the `.toc`.

- [RotateMinimap.toc](RotateMinimap.toc): the metadata and the file list. `## Interface: 16001` is Forever 1.60.1. When the client's interface number changes, update it here. Otherwise the addon shows as out of date. `## Version` stays `@project-version@` in the repo, and the release build fills in the real number. That's the BigWigs packager's token, so the packager can take over later without changes.
- [RotateMinimap.lua](RotateMinimap.lua): one frame listens for `PLAYER_LOGIN` and `PLAYER_ENTERING_WORLD` and calls `SetCVar("rotateMinimap", ROTATE)` only when the value differs. It uses no SavedVariables and has no options UI. `ROTATE` is the only setting.
- [version.yml](version.yml): the major and minor version of the next release (only `major: N` and `minor: N` lines).
- [CHANGELOG.md](CHANGELOG.md): one `## <version>` section per release, newest first, with `## Unreleased` at the top for changes not yet released. Add a line to it in every PR that changes the addon.
- `tools/`: Python with no dependencies. [check_repo.py](tools/check_repo.py) checks `version.yml`, the `.toc` and the CHANGELOG headings. [next_version.py](tools/next_version.py) prints the next version. [release_notes.py](tools/release_notes.py) prints the top CHANGELOG section for a version. [release_due.py](tools/release_due.py) says whether a release is due. [build_zip.py](tools/build_zip.py) builds `dist/RotateMinimap-<version>.zip`. [addon.py](tools/addon.py) holds the helpers they share.

If the addon ever needs more than one folder (a second addon, or dev-only folders), move it to `RotateMinimap/RotateMinimap.toc`, update `tools/addon.py`, and use `.pkgmeta` `move-folders`, as multi-addon Forever repos do.

## Checks

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
luacheck .                          # lint; .luacheckrc lists every WoW global the addon may read
python3 tools/check_repo.py         # version.yml parses; the .toc has its fields and lists every root .lua file; CHANGELOG headings in order
python3 tools/next_version.py       # the version the next release would get
python3 tools/build_zip.py 0.0.0-test && unzip -l dist/RotateMinimap-0.0.0-test.zip
```

When the addon starts using a new WoW global, add it to `read_globals` in [.luacheckrc](.luacheckrc), or luacheck fails.

## CI

[.github/workflows/checks.yml](.github/workflows/checks.yml) runs on every PR and every push to `main`. It has two jobs: `luacheck`, and `repo-checks` (compiles `tools/`, runs `check_repo.py` and `next_version.py`, and builds a test zip). The job names are the status checks the `pr-checks` ruleset requires. Renaming a job means updating the ruleset in the same change, or every PR waits for a check that never reports.

Actions are pinned to full commit SHAs, with the version in a trailing comment, as in the TF3 repos. Look up the SHA with `gh api repos/<owner>/<action>/git/ref/tags/<tag>`.

## Releasing

The steps for people are in [docs/publishing.md](docs/publishing.md): keep it in step with the workflow. In short, merging a **release PR** (one that renames CHANGELOG.md's top `## Unreleased` to the next version) publishes the release. Nothing else does.

[.github/workflows/release.yml](.github/workflows/release.yml) runs on every push to `main`, and by hand as a fallback.
- **`decide`** runs [release_due.py](tools/release_due.py). A release is due when the top CHANGELOG heading equals `next_version.py`: `major.minor` from `version.yml`, plus one past the highest `v<major>.<minor>.N` tag, or 0. Otherwise a push finishes green with a notice, and a manual run fails. The job also fails when started from any branch other than `main`.
- **`checks`** calls `checks.yml`.
- **`release`** checks the version is still free, takes the notes from that CHANGELOG section (`release_notes.py`), builds the zip, and creates the tag `v<version>` and the GitHub release together on the pushed commit.

- `check_repo.py` accepts only `Unreleased`, the next version, or the latest tag (just released) as the top heading, and fails when a released section differs from its text at its tag. So a wrong number, or an entry filed under an old version, fails on the PR, and a PR can't trigger a release by accident with a wrong number.
- Tags (`version-tags` ruleset) and releases (the repo's immutable releases setting) can't be changed once published. A bad release means a new version, not a fix in place.
- The release zip has the `RotateMinimap/` folder at its top level, holding the `.toc`, the files it lists, `LICENSE` and `CHANGELOG.md`. A wrapper folder would stop the addon loading.
- Moving to CurseForge (the BigWigs packager, `CF_API_KEY`, `## X-Curse-Project-ID`) is planned; the steps are in docs/publishing.md, "CurseForge, later".

## Testing in game

Copy `RotateMinimap.toc` and `RotateMinimap.lua` into `_forever_/Interface/AddOns/RotateMinimap/` in the game install, or unzip a release zip into `AddOns/`. A copy straight from the repo shows `@project-version@` as its version, which is harmless. The installed copy is a plain copy, not a link, so copy it again after every change. The client finds a new addon folder only after a full restart, not after `/reload`. A change to the `.lua` file shows up after `/reload`, but a change to the `.toc` needs a full restart. To check: the addon shows in the AddOn List at character select with "Load out of date AddOns" unticked, and the minimap rotates after login without a `/console rotateMinimap 1`.

## Repo rules

The rulesets match the user's TF3 mod repos and have no bypass actors, so they apply to the owner too:

- `main`: changes reach `main` only through a pull request (0 approvals needed).
- `pr-checks`: PRs into the default branch need the `luacheck` and `repo-checks` status checks to pass.
- `trunks`: `main` can't be deleted or force-pushed.
- `version-tags`: tags matching `v*.*` can't be moved or deleted once pushed.

Branch from `origin/main` as `<YYYY-MM-DD>-<slug>`. Commit, push or open a PR only when the user asks.

## Public repo

This repo is public. Keep game account names, character names, realm or server ids, home paths and machine details out of committed files. The GitHub owner name (WuphonsReach) is public and fine, for example as the `.toc` author. Write game paths starting from `_forever_/`.
