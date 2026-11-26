-- RotateMinimap: turn the rotateMinimap game setting on at each login and /reload.
-- Set ROTATE to "0" to turn it off instead.
-- The client resets the setting to 0 just after VARIABLES_LOADED. That event can come after
-- PLAYER_LOGIN, for example after a character switch. So the addon also sets the value again
-- when CVAR_UPDATE reports a change, but only until GUARD seconds after VARIABLES_LOADED.
-- A later change comes from the player (/console, or a game option in the future), and the
-- addon keeps it until the next login or /reload.
local ROTATE = "1"
local GUARD = 10 -- seconds

local guard = true -- without C_Timer, it stays on, and the addon sets every change back

local function apply()
  if GetCVar("rotateMinimap") ~= ROTATE then SetCVar("rotateMinimap", ROTATE) end
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("VARIABLES_LOADED")
f:RegisterEvent("CVAR_UPDATE") -- args: setting name, new value
f:SetScript("OnEvent", function(_, event, name)
  if event == "PLAYER_LOGIN" then
    apply()
  elseif event == "VARIABLES_LOADED" then
    if C_Timer and C_Timer.After then C_Timer.After(GUARD, function() guard = false end) end
  elseif guard and type(name) == "string" and name:lower() == "rotateminimap" then
    -- The addon's own SetCVar fires CVAR_UPDATE again. apply() then finds the value set and stops.
    apply()
  end
end)
