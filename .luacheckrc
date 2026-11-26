-- Every WoW global the addon touches must be listed here, so a typo or a stray global fails CI
-- instead of erroring in the client.
std = "lua51"
max_line_length = false
exclude_files = { ".luacheckrc", ".luarocks", "dist" }

read_globals = {
  "CreateFrame",
  "GetCVar",
  "SetCVar",
}
