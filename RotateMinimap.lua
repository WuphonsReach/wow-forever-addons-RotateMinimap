-- RotateMinimap: switch the rotateMinimap game setting on after login.
-- The client dropped it from config-cache.wtf at every login (checked 2026-11-25),
-- although `/console rotateMinimap 1` works for the session. Set ROTATE to "0" to turn off.
local ROTATE = "1"

local function apply()
  if GetCVar("rotateMinimap") ~= ROTATE then SetCVar("rotateMinimap", ROTATE) end
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("PLAYER_ENTERING_WORLD") -- again after loading screens, in case the client resets it
f:SetScript("OnEvent", apply)
