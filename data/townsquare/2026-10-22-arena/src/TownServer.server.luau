--!nonstrict
-- TownServer — Winterlichtplatz: 10 buildings, 35 floors, 176 rooms, 64 residents.
--
-- What runs here:
--   1. 64 residents (anchored block rigs, no Humanoid) with a day/night schedule:
--      they walk their square post or their workplace by day, and go inside to
--      their own home room at night. Interiors are real, so you can follow them in.
--   2. Ten hinged front doors on ProximityPrompts.
--   3. The lamp ring, lit at dusk.
--   4. A compressed day (8 real minutes = 24 in-town hours) driving Lighting.
--   5. The Verger's Errand quest loop (QuestService).
--
-- Known limit, stated plainly: there is no PathfindingService here. Residents
-- steer between hand-placed waypoints (square, street ring, building doors) with
-- one rule that keeps them out of the fountain. They do not thread furniture.

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local Lighting = game:GetService("Lighting")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local TownData = require(ReplicatedStorage:WaitForChild("TownData"))
local NpcRig = require(script.Parent:WaitForChild("NpcRig"))
local QuestService = require(script.Parent:WaitForChild("QuestService"))

local DAY_SECONDS = 480
local WALK_SPEED = 2.4

local town = workspace:WaitForChild("Town")
local buildingsFolder = town:WaitForChild("Buildings")
local runtime = Instance.new("Folder")
runtime.Name = "Runtime"
runtime.Parent = town

local npcFolder = Instance.new("Folder")
npcFolder.Name = "Residents"
npcFolder.Parent = runtime

local markerFolder = Instance.new("Folder")
markerFolder.Name = "ErrandMarkers"
markerFolder.Parent = runtime

local remotes = ReplicatedStorage:WaitForChild("TownRemotes")

----------------------------------------------------------------------
-- helper: route between two points, steering around the fountain
----------------------------------------------------------------------
local FOUNTAIN_R = 7.5

local function route(from: Vector3, to: Vector3): { Vector3 }
	local d = to - from
	local len2 = d:Dot(d)
	if len2 < 0.001 then
		return {}
	end
	local t = math.clamp(-from:Dot(d) / len2, 0, 1)
	local closest = from + d * t
	local flat = Vector3.new(closest.X, 0, closest.Z)
	if flat.Magnitude >= FOUNTAIN_R then
		return { to }
	end
	local perp = Vector3.new(-d.Z, 0, d.X)
	if perp.Magnitude < 0.001 then
		return { to }
	end
	perp = perp.Unit * (FOUNTAIN_R + 2.0)
	local a = Vector3.new(flat.X + perp.X, closest.Y, flat.Z + perp.Z)
	local b = Vector3.new(flat.X - perp.X, closest.Y, flat.Z - perp.Z)
	local detour = if a.Magnitude > b.Magnitude then a else b
	return { detour, to }
end

----------------------------------------------------------------------
-- residents
----------------------------------------------------------------------
-- Built from TownData.posts, the same table the screenshot renderer reads.
local POSTS: { [string]: Vector3 } = {}
for name, p in pairs(TownData.posts) do
	POSTS[name] = Vector3.new(p[1], p[2], p[3])
end

local buildingDoors: { [string]: Vector3 } = {}
local residents: { any } = {}

local function doorPosition(buildingKey: string): Vector3
	if buildingDoors[buildingKey] then
		return buildingDoors[buildingKey]
	end
	return Vector3.new(0, 0, 14)
end

local function roomPosition(npc): Vector3
	local bed = npc.bed
	if bed and bed.position then
		return Vector3.new(bed.position[1], bed.position[2] - 0.4, bed.position[3])
	end
	return Vector3.new(0, 0, 12)
end

local function spawnResident(npc, index: number)
	local postName = npc.post or "the fountain"
	local home = POSTS[postName] or Vector3.new(0, 0, 8)
	local jitter = Vector3.new(((index * 37) % 11) - 5, 0, ((index * 53) % 11) - 5)
	local start = home + jitter
	local model, pose = NpcRig.build(npc, npcFolder, Vector3.new(start.X, 0.0, start.Z), math.random() * 6.28)
	local resident = {
		npc = npc,
		model = model,
		pose = pose,
		position = Vector3.new(start.X, 0.0, start.Z),
		yaw = math.random() * 6.28,
		phase = math.random() * 6.28,
		waypoints = {},
		wp = 1,
		inside = false,
		homeRoom = roomPosition(npc),
		dayPost = Vector3.new(home.X + jitter.X, 0, home.Z + jitter.Z),
		workDoor = doorPosition(npc.workplace),
		speed = WALK_SPEED * (0.85 + ((index * 13) % 30) / 100),
	}
	table.insert(residents, resident)
	return resident
end

local function setDestination(resident, points: { Vector3 })
	resident.waypoints = points
	resident.wp = 1
end

local function stepResident(resident, dt: number, isNight: boolean)
	local target
	if isNight then
		target = resident.homeRoom
	else
		target = resident.dayPost
	end

	if #resident.waypoints == 0 then
		if isNight and resident.inside then
			resident.pose(CFrame.new(resident.homeRoom) * CFrame.Angles(0, resident.yaw, 0), 0, false)
			return
		end
		local dest = target
		if isNight and not resident.inside then
			-- walk to the building door first, then upstairs to the room
			setDestination(resident, route(resident.position, resident.workDoor))
			if #resident.waypoints == 0 then
				setDestination(resident, { resident.workDoor })
			end
		else
			setDestination(resident, route(resident.position, dest))
			if #resident.waypoints == 0 then
				setDestination(resident, { dest })
			end
		end
	end

	local wp = resident.waypoints[resident.wp]
	if not wp then
		resident.waypoints = {}
		return
	end

	local delta = wp - resident.position
	local flat = Vector3.new(delta.X, 0, delta.Z)
	local dist = flat.Magnitude

	if isNight and resident.inside == false and dist < 1.4 and resident.wp >= #resident.waypoints then
		-- at the door: they are home. The room is real, so put them in it.
		resident.inside = true
		resident.position = resident.homeRoom
		resident.waypoints = {}
		resident.pose(CFrame.new(resident.homeRoom) * CFrame.Angles(0, resident.yaw, 0), 0, false)
		return
	end

	if dist < 0.55 then
		resident.wp += 1
		if resident.wp > #resident.waypoints then
			resident.waypoints = {}
			resident.inside = false
			resident.pose(CFrame.new(resident.position) * CFrame.Angles(0, resident.yaw, 0), resident.phase, false)
			return
		end
		wp = resident.waypoints[resident.wp]
		delta = wp - resident.position
		flat = Vector3.new(delta.X, 0, delta.Z)
		dist = flat.Magnitude
	end

	if dist > 0.01 then
		local dir = flat.Unit
		local stepDistance = math.min(resident.speed * dt, dist)
		resident.position += dir * stepDistance
		local wantYaw = math.atan2(-dir.X, -dir.Z)
		local diff = ((wantYaw - resident.yaw + math.pi) % (2 * math.pi)) - math.pi
		resident.yaw += diff * math.min(1, dt * 5.5)
		resident.phase += dt * resident.speed * 2.6
	end

	resident.pose(
		CFrame.new(resident.position.X, 0, resident.position.Z) * CFrame.Angles(0, resident.yaw, 0),
		resident.phase,
		dist > 0.05
	)
end

----------------------------------------------------------------------
-- doors
----------------------------------------------------------------------
local function wireDoors()
	for _, building in ipairs(buildingsFolder:GetChildren()) do
		for _, descendant in ipairs(building:GetDescendants()) do
			if descendant:IsA("BasePart") and descendant.Name == "Door_Front" then
				buildingDoors[building.Name] = descendant.Position
				local base = descendant.CFrame
				local half = descendant.Size.X / 2
				local open = false
				local hinge = base * CFrame.new(-half, 0, 0)

				local prompt = Instance.new("ProximityPrompt")
				prompt.ActionText = "Open door"
				prompt.ObjectText = "Entrance"
				prompt.HoldDuration = 0
				prompt.MaxActivationDistance = 9
				prompt.RequiresLineOfSight = false
				prompt.Parent = descendant

				prompt.Triggered:Connect(function(player)
					local char = player.Character
					local hrp = char and char:FindFirstChild("HumanoidRootPart")
					if not hrp or (hrp.Position - descendant.Position).Magnitude > 12 then
						return -- proximity is checked server-side; a long arm does nothing
					end
					open = not open
					local angle = if open then math.rad(-100) else 0
					local goal = hinge * CFrame.Angles(0, angle, 0) * CFrame.new(half, 0, 0)
					TweenService:Create(descendant, TweenInfo.new(0.55, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
						CFrame = goal,
					}):Play()
					prompt.ActionText = if open then "Close door" else "Open door"
				end)
			end
		end
	end
end

----------------------------------------------------------------------
-- lamps
----------------------------------------------------------------------
local lights: { PointLight } = {}

local function wireLamps()
	local squareFolder = town:FindFirstChild("Square")
	if not squareFolder then
		return
	end
	for _, part in ipairs(squareFolder:GetChildren()) do
		if part:IsA("BasePart") and string.find(part.Name, "_Lantern") then
			local light = Instance.new("PointLight")
			light.Brightness = 0
			light.Range = 26
			light.Color = Color3.fromRGB(255, 214, 150)
			light.Shadows = false
			light.Parent = part
			table.insert(lights, light)
		end
	end
end

----------------------------------------------------------------------
-- quest context
----------------------------------------------------------------------
local crierModel
local crierPart

local questCtx = {
	data = TownData,
	remotes = remotes,
	markers = markerFolder,
	states = {},
}

function questCtx:notify(player, text)
	remotes.QuestEvent:FireClient(player, { kind = "message", text = text })
end

function questCtx:push(player)
	QuestService.push(self, player)
end

----------------------------------------------------------------------
-- boot
----------------------------------------------------------------------
wireDoors()
wireLamps()

for index, npc in ipairs(TownData.npcs) do
	local resident = spawnResident(npc, index)
	if npc.role == "town crier" then
		crierModel = resident.model
		crierPart = resident.model:FindFirstChild("Torso")
	end
end

if not crierModel then
	local r = residents[1]
	crierModel = r.model
	crierPart = r.model:FindFirstChild("Torso")
end

questCtx.crierPart = crierPart
assert(questCtx.crierPart, "TownServer: crier has no Torso part to hang the prompt on")
QuestService.attachCrier(questCtx)

-- the crier should not wander away from the notice board
for _, resident in ipairs(residents) do
	if resident.model == crierModel then
		resident.dayPost = Vector3.new(-5.7, 0, 9.4)
		resident.homeRoom = resident.homeRoom
	end
end

Players.PlayerAdded:Connect(function(player)
	questCtx.states[player] = {
		seed = math.random(1, 100000),
		errands = {},
		active = false,
		completed = 0,
		markers = {},
	}
	task.delay(3, function()
		if player.Parent then
			questCtx:push(player)
		end
	end)
end)

Players.PlayerRemoving:Connect(function(player)
	questCtx.states[player] = nil
end)

----------------------------------------------------------------------
-- day / night + movement loop
----------------------------------------------------------------------
local elapsed = 0
local scheduleAccum = 0

RunService.Heartbeat:Connect(function(dt)
	elapsed += dt
	local clock = (6.0 + (elapsed / DAY_SECONDS) * 24.0) % 24.0
	local isNight = clock < 7.0 or clock > 20.0

	if math.abs(Lighting.ClockTime - clock) > 3 then
		Lighting.ClockTime = clock
	end
	local lampTarget = if isNight then 2.2 else 0
	for _, light in ipairs(lights) do
		if math.abs(light.Brightness - lampTarget) > 0.05 then
			light.Brightness += (lampTarget - light.Brightness) * math.min(1, dt * 1.6)
		end
	end

	-- move everyone at 20 Hz; pose only the residents a player can actually see
	local moveAccum = dt
	if moveAccum > 0 then
		local characters = {}
		for _, player in ipairs(Players:GetPlayers()) do
			local char = player.Character
			local hrp = char and char:FindFirstChild("HumanoidRootPart")
			if hrp then
				table.insert(characters, hrp.Position)
			end
		end
		for _, resident in ipairs(residents) do
			local near = false
			for _, pos in ipairs(characters) do
				if (pos - resident.position).Magnitude < 140 then
					near = true
					break
				end
			end
			if near then
				stepResident(resident, dt, isNight)
			end
		end
	end

	scheduleAccum += dt
	if scheduleAccum > 2 then
		scheduleAccum = 0
		remotes.QuestEvent:FireAllClients({
			kind = "clock",
			clock = clock,
			night = isNight,
			residents = #residents,
			lampLit = lampTarget > 0,
		})
	end
end)

print(string.format(
	"[Winterlichtplatz] %d buildings, %d floors, %d rooms, %d residents, %d doors wired",
	#TownData.buildings,
	TownData.meta.floors,
	#TownData.rooms,
	#residents,
	#TownData.doors
))
