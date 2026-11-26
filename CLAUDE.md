# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A one-file addon for WoW Forever (client 1.60.1, `## Interface: 16001`). It switches the game's `rotateMinimap` setting (a console variable, or CVar) on at login and after every loading screen, because the Forever client drops the setting at login. The player-facing description is [README.md](README.md).

The repo is public on GitHub ([WuphonsReach/wow-forever-addons-RotateMinimap](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap), MIT). Releases are published on GitHub only, not on CurseForge yet. There is no build step and no unit tests. The client loads the `.lua` and `.toc` files as they are, and the user does every in-game test.

## Layout

The addon's files sit at the repo root, which is the usual layout for a small single-addon repo. The repo root is the addon folder, so the installed folder must be named `RotateMinimap` to match the `.toc`.

- [RotateMinimap.toc](RotateMinimap.toc): the metadata and the file list. `## Interface: 16001` is Forever 1.60.1. When the client's interface number changes, update it here. Otherwise the addon shows as out of date. `## Version` stays `@project-version@` in the repo, and the release build fills in the real number. That's the BigWigs packager's token, so the packager can take over later without changes.
- [RotateMinimap.lua](RotateMinimap.lua): one frame listens for `PLAYER_LOGIN` and `PLAYER_ENTERING_WORLD` and calls `SetCVar("rotateMinimap", ROTATE)` only when the value differs. It uses no SavedVariables and has no options UI. `ROTATE` is the only setting.
- [version.yml](version.yml): the major and minor version of the next release (only `major: N` and `minor: N` lines).
- [CHANGELOG.md](CHANGELOG.md): one `## <version>` section per release, newest first, with `## Unreleased` at the top for changes not yet released. Add a line to it in every PR that changes the addon.
- `tools/`: Python with no dependencies. [check_repo.py](tools/check_repo.py) checks `version.yml`, the `.toc` and the CHANGELOG headings. [next_version.py](tools/next_version.py) prints the next version. [release_notes.py](tools/release_notes.py) prints the top CHANGELOG section for a version. [build_zip.py](tools/build_zip.py) builds `dist/RotateMinimap-<version>.zip`. [addon.py](tools/addon.py) holds the helpers they share.

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

[.github/workflows/release.yml](.github/workflows/release.yml) is started by hand from `main` (Actions > release > Run workflow, or `gh workflow run release.yml --ref main`). It runs the checks and computes the version: `major.minor` from `version.yml`, plus a patch number one past the highest `v<major>.<minor>.N` tag, or 0 if there is none. It then checks that CHANGELOG.md's top section is headed with that version, builds the zip, and creates the tag `v<version>` and the GitHub release together, with that CHANGELOG section as the notes.

- To release: open a PR that renames `## Unreleased` to the version `python3 tools/next_version.py` prints (CI prints it too), merge it, then run the workflow. For a bigger change, bump `minor` (or `major`, with `minor` back to 0) in `version.yml` in the same PR.
- `check_repo.py` accepts only `Unreleased`, the next version, or the latest tag (just released) as the top heading, so a wrong number fails on the PR, not at release time.
- Tags (`version-tags` ruleset) and releases (the repo's immutable releases setting) can't be changed once published. A bad release means a new version, not a fix in place.
- The release zip has the `RotateMinimap/` folder at its top level, holding the `.toc`, the files it lists, `LICENSE` and `CHANGELOG.md`. A wrapper folder would stop the addon loading.

### Moving to CurseForge later

Most Forever addons on GitHub release with the [BigWigsMods packager](https://github.com/BigWigsMods/packager), which uploads to CurseForge and GitHub releases. To switch over:

- Add a `.pkgmeta` with `package-as: RotateMinimap`, a `manual-changelog` pointing at `CHANGELOG.md` (the packager posts the whole file, so trim the GitHub release notes to one section as now), and an `ignore` list for dev files (`.github`, `.pkgmeta`, `.luacheckrc`, `CLAUDE.md`, `tools`, `version.yml`).
- Add `## X-Curse-Project-ID: <id>` to the `.toc` after the project is created, and a `CF_API_KEY` repository secret.
- In `release.yml`, keep the version and tag steps, push the tag, and replace the zip and release steps with the packager.

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

This repo is public. Keep account names, character names, realm or server ids, home paths and machine details out of committed files. Write game paths starting from `_forever_/`.
