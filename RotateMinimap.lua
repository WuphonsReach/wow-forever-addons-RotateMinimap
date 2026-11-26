-- RotateMinimap: keep the rotateMinimap game setting on. Set ROTATE to "0" to turn off.
-- The client resets the setting to 0 just after VARIABLES_LOADED. That event can come after
-- PLAYER_LOGIN and PLAYER_ENTERING_WORLD, for example after a character switch. So the addon
-- also sets the value again when CVAR_UPDATE reports a change to it.
local ROTATE = "1"

local function apply()
  if GetCVar("rotateMinimap") ~= ROTATE then SetCVar("rotateMinimap", ROTATE) end
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("PLAYER_ENTERING_WORLD") -- again after loading screens
f:RegisterEvent("CVAR_UPDATE")           -- args: setting name, new value
f:SetScript("OnEvent", function(_, event, name)
  -- The addon's own SetCVar fires CVAR_UPDATE again. apply() then finds the value set and stops.
  if event ~= "CVAR_UPDATE" or (type(name) == "string" and name:lower() == "rotateminimap") then
    apply()
  end
end)
