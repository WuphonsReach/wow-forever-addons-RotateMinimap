# Publishing a release

## Summary

- To publish a release, merge a release PR. A release PR renames the top heading of CHANGELOG.md from `## Unreleased` to the next version, for example `## 0.1.1`.
- Releases go to the repo's [Releases](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap/releases) page on GitHub only. Each release has one zip, `RotateMinimap-<version>.zip`. CurseForge comes later (see [CurseForge, later](#curseforge-later)).
- The release notes are the text of that CHANGELOG section.
- Releases are permanent. You cannot move or delete a `v*.*` tag, and you cannot edit a published release. To correct a mistake, release the next version.

The [release workflow](../.github/workflows/release.yml) runs on every push to `main`. It publishes only when the top CHANGELOG heading is a version that has no tag. All other merges finish green and release nothing.

## Version numbers

- [version.yml](../version.yml) gives `major.minor`.
- The patch number is one more than the highest `v<major>.<minor>.N` tag. If there is no such tag, the patch number is 0.
- `python3 tools/next_version.py` prints the next version. CI also prints it on every PR.

## Every PR

For each change that a player can see, add a line under `## Unreleased` at the top of [CHANGELOG.md](../CHANGELOG.md).

If there is no `## Unreleased` section (for example, right after a release), add one above the newest version. CI fails a PR that adds lines under a released version.

## Release a version

1. Make a branch from `main`, named `<YYYY-MM-DD>-release-<version>`.
2. Run `python3 tools/next_version.py` to get the version.
   - For a fix, use that version. For example, `0.1.1` follows `0.1.0`.
   - For a larger change, increase `minor` in `version.yml`, for example `minor: 2` for 0.2.0. Or increase `major` and set `minor: 0`. Then run the script again.
3. In CHANGELOG.md, change `## Unreleased` to `## <version>`.
4. Read the section again. The release notes use its text exactly.
5. Open the PR. CI makes sure that the heading is the next version.
6. Merge the PR when the checks pass. The merge starts the `release` workflow (see the Actions tab), which has these jobs:
   - `decide` finds the version heading and reports "Release due".
   - `checks` runs luacheck and the repo checks again.
   - `release` builds the zip. Then it creates the tag `v<version>` and the GitHub release "Rotate Minimap (Forever) \<version\>".
7. On the Releases page, examine the title, the notes and the zip.
8. Download the zip and examine it:
   - It has a `RotateMinimap/` folder at the top level.
   - The folder holds these files:
     - `RotateMinimap.toc`
     - `RotateMinimap.lua`
     - `LICENSE`
     - `CHANGELOG.md`
   - The `.toc` file reads `## Version: <version>`.
9. Unzip the zip into `_forever_/Interface/AddOns/` and restart the game. Make sure that the addon loads and that the minimap rotates after login.

After a release, the top CHANGELOG heading is the released version. This is correct, and the next merge publishes nothing. The next PR that changes the addon adds a new `## Unreleased` section.

## Problems

### The release run failed

The run shows red in the Actions tab. Read the log of the step that failed.

- If the failure came before the "Create the tag and release" step, the workflow published nothing. Correct the cause in a PR. When that PR merges, the release occurs, because the top heading still has the unreleased version.
- To try again with no change, for example after a GitHub outage, start the workflow manually. Use Actions > release > Run workflow on `main`, or run `gh workflow run release.yml --ref main`.

### A manual run fails with "No release: …"

The top heading is not the next version. A manual run releases only what a release PR has prepared.

### A merge did not release, but it should have

Open the `decide` job of the run. Its notice gives the reason, for example "top section is '## Unreleased'".

Release runs wait in a queue, one at a time, and GitHub keeps only one waiting run. If two merges occur quickly, GitHub can cancel the waiting run. In that case, start the workflow manually.

### The published release is wrong

You cannot edit or delete it. Correct it in the next version: add an entry under `## Unreleased`, then merge a release PR for the next patch number.

## CurseForge, later

On CurseForge, the project will have the name Rotate Minimap (Forever), under the account WuphonsReach.

Most Forever addons on GitHub use the [BigWigsMods packager](https://github.com/BigWigsMods/packager) for releases. In one run, it uploads to CurseForge and to GitHub releases. To change to the packager:

1. On CurseForge, create the project manually.
   - Examine the slug that CurseForge gives (probably `rotate-minimap-forever`). It becomes part of the project's address.
   - Write down the project id from the project page.
2. In the CurseForge author settings, create an API token.
3. Store the token as the repository secret `CF_API_KEY` (GitHub repo > Settings > Secrets and variables > Actions).
4. In a PR, add `## X-Curse-Project-ID: <id>` to `RotateMinimap.toc`.
5. In the same PR, add a `.pkgmeta` file:
   - `package-as: RotateMinimap`.
   - `manual-changelog`, set to `CHANGELOG.md`.
   - An `ignore` list for the development files:
     - `.github`
     - `.pkgmeta`
     - `.luacheckrc`
     - `CLAUDE.md`
     - `docs`
     - `tools`
     - `version.yml`
6. In the same PR, change `release.yml`:
   - Keep the `decide` and `checks` jobs.
   - In the release job, push the tag, then run the packager. The packager replaces the zip step and the `gh release create` step.
   - The packager puts the full CHANGELOG on CurseForge. Keep the GitHub release notes to one section, as now.

The release PR process does not change. After the change, a merged release PR publishes to GitHub and to CurseForge.
