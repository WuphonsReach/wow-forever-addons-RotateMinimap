# RotateMinimap

A tiny addon for WoW Forever (client 1.60.1, `## Interface: 16001`) that switches the `rotateMinimap` game setting on at login and after loading screens, so the minimap turns with your facing.

## Why

`/console rotateMinimap 1` works for the session, but on the Forever client the setting was gone from `config-cache.wtf` after the next login (checked 2026-11-25). The client resets it, and no other addon or OneForAll option sets it. This addon sets it again each time.

## Install

Download the zip from the newest [release](https://github.com/WuphonsReach/wow-forever-addons-RotateMinimap/releases) and unzip it into the game's `Interface/AddOns/` (`_forever_/Interface/AddOns/`). It holds a `RotateMinimap` folder, which must sit directly in `AddOns/`. Or copy `RotateMinimap.toc` and `RotateMinimap.lua` into a folder named `RotateMinimap` there. A new addon folder is found after a full restart, not `/reload`. It should then show in the AddOn List.

## Settings

None. To turn rotation off, change `ROTATE` to `"0"` in `RotateMinimap.lua`. It uses no SavedVariables.

## License

MIT, see `LICENSE`.
