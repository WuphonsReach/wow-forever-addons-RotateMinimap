# Development and local testing

## Summary

- Link the repo folder into the game's `AddOns` folder. The game then loads the files that you edit, with no copy step.
- After a change to the `.lua` file, type `/reload` in the game. After a change to the `.toc` file, restart the game fully.
- Before you open a PR, run luacheck and `tools/check_repo.py`. CI runs the same checks.

For releases, see [publishing.md](publishing.md).

## Requirements

- The WoW Forever client, version 1.60.1.
- Git.
- Python 3. The scripts in `tools/` need no packages.
- luacheck, a Lua linter. To install it with LuaRocks:

  ```bash
  luarocks install --local luacheck
  export PATH="$HOME/.luarocks/bin:$PATH"
  ```

## Link the repo into the game

The repo root is the addon folder. The link must have the name `RotateMinimap`, the same as the `.toc` file.

1. Close the game.
2. If `_forever_/Interface/AddOns/` has a `RotateMinimap` folder, move it out.
3. Make the link, as shown below for your system.
4. Start the game fully. The game finds a new addon folder only after a full restart, not after `/reload`.

On Linux (Wine or Lutris), use a symbolic link. Wine follows it.

```bash
ln -s /path/to/repo "<game folder>/_forever_/Interface/AddOns/RotateMinimap"
```

On Windows, use a directory junction in Command Prompt. A junction needs no administrator rights.

```bat
mklink /J "<game folder>\_forever_\Interface\AddOns\RotateMinimap" "C:\path\to\repo"
```

Things to know about the link:

- The game loads the branch that is checked out. After you change branches, `/reload` or restart the game.
- The folder also holds the other repo files, for example `.git`, `docs` and `tools`. The client loads only the files that the `.toc` lists, so the other files do no harm.
- The AddOn List shows the version as `@project-version@`. This is correct for files from the repo. The release build writes the real number.

## Test a change

1. Restart the game or type `/reload`:
   - After a change to the `.lua` file, `/reload` is sufficient.
   - After a change to the `.toc` file, restart the game fully.
2. At character select, open the AddOn List. Clear "Load out of date AddOns".
3. Make sure that Rotate Minimap (Forever) is in the list and on. If it shows as out of date, `## Interface` in the `.toc` does not match the client.
4. Log in. Make sure that the minimap rotates with your facing. Do not type `/console rotateMinimap 1`.
5. Go through a loading screen, for example an instance portal. Make sure that the minimap still rotates.
6. Log out to character select and log in with a different character. Make sure that the minimap rotates. A character switch is the case that failed in 0.1.0.
7. Type `/reload`. Make sure that the minimap still rotates. A UI reload also resets the setting.
8. Log out and log in again. Make sure that the minimap rotates.
9. Wait 10 seconds after login, then type `/console rotateMinimap 0`. Make sure that the minimap stops rotating and stays north-up, also after a loading screen. The addon must not set the player's change back.
10. Type `/reload`. Make sure that the minimap rotates again.

## Run the checks

```bash
luacheck .                      # lint
python3 tools/check_repo.py     # version.yml, the .toc and the CHANGELOG headings
python3 tools/next_version.py   # the version that the next release gets
```

luacheck fails when the code uses a WoW global that is not in `read_globals` in [.luacheckrc](../.luacheckrc). When the addon starts to use a new WoW global, add it there.

For each change that a player can see, add a line under `## Unreleased` in [CHANGELOG.md](../CHANGELOG.md).

## Test a release zip

Do this test when you change `tools/build_zip.py` or the files that the `.toc` lists.

1. Build a test zip:

   ```bash
   python3 tools/build_zip.py 0.0.0-test
   unzip -l dist/RotateMinimap-0.0.0-test.zip
   ```

2. Make sure that the zip has a `RotateMinimap/` folder at the top level, with no wrapper folder around it.
3. Close the game and remove the link. This removes only the link, not the repo.
   - On Linux: `rm "<game folder>/_forever_/Interface/AddOns/RotateMinimap"`. Do not add a `/` at the end.
   - On Windows: `rmdir "<game folder>\_forever_\Interface\AddOns\RotateMinimap"`.
4. Unzip the zip into `_forever_/Interface/AddOns/`.
5. Start the game, and do the steps in [Test a change](#test-a-change). The AddOn List shows the version as `0.0.0-test`.
6. Close the game. Delete the unzipped `RotateMinimap` folder, and make the link again.
