--!nonstrict
-- QuestService — "The Verger's Errand", a three-stop delivery loop.
--
-- The point of the quest is to make a claim the town can keep: every one of the
-- ten buildings is enterable, has a stair, and its upper floors are reachable on
-- foot. So each errand marker is placed at the centre of a real upper-floor room,
-- and the only way to finish it is to walk up the stairs and stand in the room.
--
-- Server-authoritative: the client is told what to do and is never trusted with
-- whether it happened. Marker triggers are validated against the player's
-- distance to the marker before credit is given.

local QuestService = {}

local ERRANDS = 3
local INTERACT_RANGE = 9.0

local function count(t: { [any]: any }): number
	local n = 0
	for _ in pairs(t) do
		n += 1
	end
	return n
end

--- Build the errand plan for one player: deterministic, distinct buildings,
--- upper floor only (so the stairs are always part of the job).
function QuestService.plan(data: table, seed: number): { any }
	local candidates = {}
	for _, room in ipairs(data.rooms) do
		if room.floor >= 2 then
			table.insert(candidates, room)
		end
	end
	local picked = {}
	local usedBuildings = {}
	local i = (seed * 7) % #candidates + 1
	local guard = 0
	while count(picked) < ERRANDS and guard < #candidates * 4 do
		guard += 1
		local room = candidates[i]
		i = i % #candidates + 1
		if room and not usedBuildings[room.building] then
			usedBuildings[room.building] = true
			table.insert(picked, room)
		end
	end
	local out = {}
	for index, room in ipairs(picked) do
		out[index] = {
			index = index,
			building = room.building,
			floor = room.floor,
			label = room.label,
			centre = Vector3.new(room.centre[1], room.centre[2], room.centre[3]),
			done = false,
		}
	end
	return out
end

local function buildingName(data: table, key: string): string
	for _, b in ipairs(data.buildings) do
		if b.key == key then
			return b.name
		end
	end
	return key
end

--- Spawn the visible marker for an errand and wire its prompt.
function QuestService.makeMarker(ctx, errand): Part
	local marker = Instance.new("Part")
	marker.Name = "ErrandMarker_" .. errand.index
	marker.Size = Vector3.new(0.9, 0.9, 0.9)
	marker.Position = errand.centre
	marker.Anchored = true
	marker.CanCollide = false
	marker.CanQuery = false
	marker.Material = Enum.Material.Neon
	marker.Color = Color3.fromRGB(255, 214, 112)
	marker.Transparency = 0.25
	marker.Parent = ctx.markers

	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = "Deliver parcel"
	prompt.ObjectText = errand.label .. ", " .. buildingName(ctx.data, errand.building)
	prompt.HoldDuration = 0.6
	prompt.MaxActivationDistance = 8
	prompt.RequiresLineOfSight = false
	prompt.Parent = marker

	prompt.Triggered:Connect(function(player)
		local state = ctx.states[player]
		if not state or not state.active then
			return
		end
		local mine = state.errands[errand.index]
		if not mine or mine.done then
			return
		end
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart")
		if not root then
			return
		end
		if (root.Position - errand.centre).Magnitude > INTERACT_RANGE then
			return -- client-side teleports and long arms do not count
		end
		mine.done = true
		marker.Transparency = 1
		prompt.Enabled = false
		ctx:push(player)
	end)

	return marker
end

--- The crier's prompt starts (or restarts) the errand.
function QuestService.attachCrier(ctx)
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = "Ask about the errands"
	prompt.ObjectText = "Town Crier"
	prompt.HoldDuration = 0.25
	prompt.MaxActivationDistance = 10
	prompt.RequiresLineOfSight = false
	prompt.Parent = ctx.crierPart

	prompt.Triggered:Connect(function(player)
		local state = ctx.states[player]
		if not state then
			state = {
				seed = math.random(1, 100000),
				errands = {},
				active = false,
				completed = 0,
				markers = {},
			}
			ctx.states[player] = state
		end
		if not state.active then
			for _, marker in ipairs(state.markers) do
				marker:Destroy()
			end
			state.markers = {}
			state.errands = QuestService.plan(ctx.data, state.seed + state.completed)
			state.active = true
			for _, errand in ipairs(state.errands) do
				table.insert(state.markers, QuestService.makeMarker(ctx, errand))
			end
			ctx:notify(player, "The verger hands you three parcels. Doors are open; the stairs are at the back.")
		end
		ctx:push(player)
	end)
end

--- Credit check + completion. Called from the push handler and on join.
function QuestService.push(ctx, player)
	local state = ctx.states[player]
	if not state then
		return
	end
	local done = 0
	for _, errand in ipairs(state.errands) do
		if errand.done then
			done += 1
		end
	end
	if state.active and done >= #state.errands and #state.errands > 0 then
		state.active = false
		state.completed += 1
		for _, marker in ipairs(state.markers) do
			marker:Destroy()
		end
		state.markers = {}
		ctx:notify(player, string.format("All three parcels delivered. The verger owes you a drink. (%d run(s) done)", state.completed))
	end
	local payload = {
		kind = "state",
		active = state.active,
		completed = state.completed,
		errands = {},
		done = done,
		total = #state.errands,
	}
	for _, errand in ipairs(state.errands) do
		table.insert(payload.errands, {
			index = errand.index,
			building = buildingName(ctx.data, errand.building),
			floor = errand.floor,
			label = errand.label,
			done = errand.done,
			position = { errand.centre.X, errand.centre.Y, errand.centre.Z },
		})
	end
	ctx.remotes.QuestEvent:FireClient(player, payload)
end

return QuestService
