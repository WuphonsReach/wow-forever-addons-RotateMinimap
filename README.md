# Rotate Minimap (Forever)

<img src="media/icon-curseforge-400.png" alt="The addon icon: a compass face with the player arrow pointing up and the N turned away from the top" width="128" align="right">

This addon makes the minimap turn with your facing, instead of keeping north at the top. It is for WoW Forever (client 1.60.1) only.

The game has a `rotateMinimap` setting, but the Forever client resets it at every login and `/reload`. The addon turns the setting on again after each reset.

## Before and after

Both pictures show the same place, with the player facing west. The left picture is without the addon, and the right picture is with it.

<img src="media/minimap-before-after.png" alt="Two minimaps side by side. Left, without the addon: the north marker is at the top of the rim, and the player arrow points left. Right, with the addon: the player arrow points up, the map is turned, and the north marker is on the right of the rim." width="471">

- Without the addon, the map stays fixed with north at the top, and the player arrow turns. The small triangle on the rim marks north.
- With the addon, the player arrow always points up, and the map turns around it. Here the north marker is on the right, because the player faces west.

## Install

1. Download the zip from the newest [release](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap/releases).
2. Unzip it into `_forever_/Interface/AddOns/`. The zip holds a `RotateMinimap` folder, and that folder must be directly in `AddOns/`.
3. Close the game and start it again. The game finds a new addon folder only after a full restart, not after `/reload`.
4. At character select, open the AddOn List and make sure that Rotate Minimap (Forever) is in the list and on.

You can also install from the repo. Make a folder named `RotateMinimap` in `AddOns/`, and copy `RotateMinimap.toc`, `RotateMinimap.lua` and `icon.tga` into it. To change the addon and test it, see [docs/development.md](docs/development.md).

## Settings

The addon has no options and saves no data.

- To stop the rotation for the rest of the session, type `/console rotateMinimap 0`. The addon leaves your change alone until the next login or `/reload`.
- To stop it for good, turn the addon off in the AddOn List.

## Other WoW versions

Other WoW versions have a "Rotate Minimap" checkbox in their interface options, so they do not need this addon. Forever has the setting but no checkbox.

## Why the addon is necessary

The command `/console rotateMinimap 1` turns rotation on, but only until you log out. After the next login, the setting is gone from `config-cache.wtf`. No other addon or OneForAll option sets it again. This was found on 2026-11-25.

## License

MIT. See [LICENSE](LICENSE).
