# Publishing a release

## In short

- **Where releases go.** GitHub only for now, on the repo's [Releases](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap/releases) page. Each release has one zip, `RotateMinimap-<version>.zip`. CurseForge comes later (see [CurseForge, later](#curseforge-later)).
- **What triggers one.** Merging a **release PR**: a PR that renames CHANGELOG.md's top heading from `## Unreleased` to the next version, for example `## 0.1.1`. The [release workflow](../.github/workflows/release.yml) runs on every push to `main` and publishes only when the top heading is a version that has no tag yet. Every other merge finishes green without releasing anything.
- **The version number.** `major.minor` comes from [version.yml](../version.yml). The patch number is one past the highest existing `v<major>.<minor>.N` tag, or 0 if there is none. `python3 tools/next_version.py` prints it, and CI prints it on every PR.
- **The release notes** are the text of that CHANGELOG section.
- **No take-backs.** Tags matching `v*.*` can't be moved or deleted, and releases can't be edited once published. A mistake means releasing the next version, not fixing this one.

## Day to day: every PR

Add a line under `## Unreleased` at the top of [CHANGELOG.md](../CHANGELOG.md) for anything a player would notice. If there is no `## Unreleased` section (right after a release), add one above the newest version. CI fails a PR that adds lines under a version that's already released.

## Releasing a version

1. **Start a branch** from `main`, named `<YYYY-MM-DD>-release-<version>`.
2. **Find the version.** Run `python3 tools/next_version.py`.
   - For a fix, that's the version (`0.1.0` is followed by `0.1.1`).
   - For a bigger change, bump `minor` in `version.yml` (`minor: 2` for 0.2.0), or bump `major` and set `minor: 0`, and run it again.
3. **Rename the heading.** In CHANGELOG.md, change `## Unreleased` to `## <version>`. Read the section over: it becomes the release notes word for word.
4. **Open the PR.** CI checks that the heading is the next version. Merge it once the checks pass.
5. **The release publishes itself.** The merge starts the `release` workflow (Actions tab). Its jobs:
   - `decide` sees the version heading and reports "Release due".
   - `checks` runs luacheck and the repo checks again.
   - `release` builds the zip and creates the tag `v<version>` and the GitHub release, titled "Rotate Minimap (Forever) \<version\>".
6. **Check the release.** On the Releases page, check the title, the notes and the zip. Download the zip and check that it holds a `RotateMinimap/` folder with `RotateMinimap.toc`, `RotateMinimap.lua`, `LICENSE` and `CHANGELOG.md`, and that the `.toc` reads `## Version: <version>`. Then install it in the game (unzip into `_forever_/Interface/AddOns/`, restart) and check that it loads and the minimap rotates after login.

After a release, CHANGELOG.md's top heading is the released version, and that's a valid state: the next merge publishes nothing. The next PR that changes the addon adds a new `## Unreleased` section.

## When something goes wrong

- **The release run failed** (red in the Actions tab). Read the failing step's log.
  - If it failed before "Create the tag and release", nothing was published. Fix the cause in a PR. The release happens when that PR merges, because the top heading still names the unreleased version.
  - To retry without a change, for example after a GitHub outage, run it by hand: Actions > release > Run workflow on `main`, or `gh workflow run release.yml --ref main`.
- **A manual run fails with "No release: …".** The top heading isn't the next version. A manual run only releases what a release PR has set up.
- **A merge didn't release, but should have.** Open the run's `decide` job: its notice gives the reason, for example "top section is '## Unreleased'". Release runs queue one at a time, and GitHub keeps only one waiting run, so two merges in quick succession can drop the waiting one. Run the workflow by hand.
- **The published release is wrong.** It can't be edited or deleted. Fix it in the next version: an `## Unreleased` entry, then a release PR for the next patch number.

## CurseForge, later

The project is to be called **Rotate Minimap (Forever)** on CurseForge, under the account WuphonsReach. Most Forever addons on GitHub release with the [BigWigsMods packager](https://github.com/BigWigsMods/packager), which uploads to CurseForge and to GitHub releases in one run. To switch over:

1. **On CurseForge** (by hand): create the project. Check the slug it suggests (probably `rotate-minimap-forever`), since it's part of the project's address. Note the project id from the project page.
2. **Create an API token** in the CurseForge author settings, and store it as the repository secret `CF_API_KEY` (GitHub repo > Settings > Secrets and variables > Actions).
3. **In a PR:**
   - Add `## X-Curse-Project-ID: <id>` to `RotateMinimap.toc`.
   - Add a `.pkgmeta` with `package-as: RotateMinimap`, `manual-changelog` pointing at `CHANGELOG.md`, and an `ignore` list for dev files (`.github`, `.pkgmeta`, `.luacheckrc`, `CLAUDE.md`, `docs`, `tools`, `version.yml`).
   - In `release.yml`, keep the `decide` and `checks` jobs. Have the release job push the tag, then run the packager instead of the zip and `gh release create` steps. The packager posts the whole CHANGELOG to CurseForge, so trim the GitHub release notes to one section, as now.
4. **The release PR process stays the same.** A merged release PR then publishes to both GitHub and CurseForge.
