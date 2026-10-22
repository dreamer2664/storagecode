--!nonstrict
-- NpcRig — builds one resident from anchored blocks and animates it without a
-- Humanoid. 64 of these live in the square; a Humanoid each would cost far more
-- than a town this size needs, and anchored rigs replicate predictably.
--
-- Rig layout (metres, +Y up, facing -Z at yaw 0):
--   Root(primary, invisible) -> Torso, Head, ArmL/ArmR, LegL/LegR, Hat?
-- Every part is Anchored, so there are no welds to break and no physics cost;
-- NpcRig.pose() writes CFrames from a root CFrame + walk phase.

local NpcRig = {}

local SIZES = {
	Torso = Vector3.new(0.92, 1.15, 0.52),
	Head = Vector3.new(0.56, 0.56, 0.56),
	Arm = Vector3.new(0.26, 1.02, 0.28),
	Leg = Vector3.new(0.30, 1.02, 0.32),
	Hat = Vector3.new(0.66, 0.22, 0.66),
}

local HIP_Y = -0.55 -- hip joint, relative to torso centre
local SHOULDER_Y = 0.42

local function makePart(name: string, size: Vector3, colour: Color3, material: Enum.Material, parent: Instance): Part
	local p = Instance.new("Part")
	p.Name = name
	p.Size = size
	p.Color = colour
	p.Material = material
	p.Anchored = true
	p.CanCollide = false
	p.CanQuery = false
	p.CanTouch = false
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.Parent = parent
	return p
end

--- Build a resident rig. Returns a model with the parts plus a `pose` closure.
function NpcRig.build(npc: table, parent: Instance, position: Vector3, facingYaw: number)
	local model = Instance.new("Model")
	model.Name = "NPC_" .. tostring(npc.id)

	local skin = Color3.fromRGB(npc.skin[1], npc.skin[2], npc.skin[3])
	local shirt = Color3.fromRGB(npc.shirt[1], npc.shirt[2], npc.shirt[3])
	local trousers = Color3.fromRGB(npc.trousers[1], npc.trousers[2], npc.trousers[3])
	local height = npc.height or 1.7
	local scale = height / 1.75

	local root = makePart("Root", Vector3.new(0.4, 0.4, 0.4), Color3.new(0, 0, 0), Enum.Material.SmoothPlastic, model)
	root.Transparency = 1
	root.CanCollide = false

	local torso = makePart("Torso", SIZES.Torso * scale, shirt, Enum.Material.Fabric, model)
	local head = makePart("Head", SIZES.Head * scale, skin, Enum.Material.SmoothPlastic, model)
	local armL = makePart("ArmL", SIZES.Arm * scale, shirt, Enum.Material.Fabric, model)
	local armR = makePart("ArmR", SIZES.Arm * scale, shirt, Enum.Material.Fabric, model)
	local legL = makePart("LegL", SIZES.Leg * scale, trousers, Enum.Material.Fabric, model)
	local legR = makePart("LegR", SIZES.Leg * scale, trousers, Enum.Material.Fabric, model)

	local hat = nil
	if npc.hat then
		hat = makePart("Hat", SIZES.Hat * scale, Color3.fromRGB(58, 48, 42), Enum.Material.Wood, model)
	end

	model.PrimaryPart = root
	model.Parent = parent

	local function pose(cf: CFrame, phase: number, moving: boolean)
		local swing = 0.0
		if moving then
			swing = math.sin(phase) * 0.55
		end
		local bob = moving and math.abs(math.sin(phase)) * 0.045 or 0.0

		local base = cf * CFrame.new(0, bob, 0) * CFrame.new(0, 0.98 * scale, 0)
		root.CFrame = cf * CFrame.new(0, 0.98 * scale, 0)

		torso.CFrame = base
		head.CFrame = base * CFrame.new(0, (SIZES.Torso.Y * 0.5 + SIZES.Head.Y * 0.5) * scale + 0.04, 0)
		if hat then
			hat.CFrame = head.CFrame * CFrame.new(0, SIZES.Head.Y * 0.5 * scale + 0.05, 0)
		end

		local shoulder = base * CFrame.new(0, SHOULDER_Y * scale, 0)
		armL.CFrame = shoulder * CFrame.Angles(-swing * 0.65, 0, 0.06) * CFrame.new(0, -0.5 * scale, 0)
		armR.CFrame = shoulder * CFrame.Angles(swing * 0.65, 0, -0.06) * CFrame.new(0, -0.5 * scale, 0)

		local hip = base * CFrame.new(0, HIP_Y * scale, 0)
		legL.CFrame = hip * CFrame.Angles(swing, 0, 0) * CFrame.new(-0.18 * scale, -0.5 * scale, 0)
		legR.CFrame = hip * CFrame.Angles(-swing, 0, 0) * CFrame.new(0.18 * scale, -0.5 * scale, 0)
	end

	pose(CFrame.new(position) * CFrame.Angles(0, facingYaw, 0), 0, false)
	return model, pose
end

return NpcRig
