-- Loads the generated TownData module under plain Luau (no Roblox) and asserts
-- the town's own claims about itself. Run: luau tests/check_towndata.luau
local data = require("../src/ReplicatedStorage/TownData")
local fails = {}
local function check(cond, msg) if not cond then table.insert(fails, msg) end end

check(#data.buildings == 10, "expected 10 buildings, got " .. #data.buildings)
check(#data.npcs == 64, "expected 64 residents, got " .. #data.npcs)
check(#data.doors == 10, "expected 10 doors, got " .. #data.doors)

-- every building is 3 or 4 floors, with interiors actually scheduled
local perBuilding, rooms = {}, {}
for _, r in ipairs(data.rooms) do
	rooms[r.building] = (rooms[r.building] or 0) + 1
	perBuilding[r.building] = math.max(perBuilding[r.building] or 0, r.floor)
end
for _, b in ipairs(data.buildings) do
	local f = perBuilding[b.key]
	check(f == b.floors, b.key .. ": highest room floor " .. tostring(f) .. " != declared " .. b.floors)
	check(f == 3 or f == 4, b.key .. ": floors must be 3 or 4, got " .. tostring(f))
	check((rooms[b.key] or 0) >= 10, b.key .. ": only " .. tostring(rooms[b.key]) .. " rooms")
end

local beds = 0
for _, n in ipairs(data.npcs) do
	if n.bed then beds = beds + 1 end
	check(n.home_floor and n.home_floor >= 1, n.id .. " has no home floor")
end
check(beds == #data.npcs, beds .. "/" .. #data.npcs .. " residents have a bed")

print(string.format("check_towndata: buildings=%d floors=%d rooms=%d residents=%d beds=%d",
	#data.buildings, data.meta.floors, #data.rooms, #data.npcs, beds))
if #fails > 0 then
	for _, f in ipairs(fails) do print("  FAIL " .. f) end
	print("check_towndata: FAIL (" .. #fails .. ")")
	os.exit(1)
end
print("check_towndata: PASS")
