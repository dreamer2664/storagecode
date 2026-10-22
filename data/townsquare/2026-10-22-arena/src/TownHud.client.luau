--!nonstrict
-- TownHud — clock, errand list with live distances, and the crier's messages.
-- Everything shown here is pushed by the server; the client never decides that
-- an errand is done.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local remotes = ReplicatedStorage:WaitForChild("TownRemotes")
local questEvent = remotes:WaitForChild("QuestEvent")

local gui = Instance.new("ScreenGui")
gui.Name = "TownHud"
gui.ResetOnSpawn = false
gui.IgnoreGuiInset = true
gui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
gui.Parent = player:WaitForChild("PlayerGui")

local function panel(parent, size, position, colour)
	local f = Instance.new("Frame")
	f.Size = size
	f.Position = position
	f.BackgroundColor3 = colour or Color3.fromRGB(18, 20, 24)
	f.BackgroundTransparency = 0.18
	f.BorderSizePixel = 0
	f.Parent = parent
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, 6)
	corner.Parent = f
	local stroke = Instance.new("UIStroke")
	stroke.Color = Color3.fromRGB(96, 104, 120)
	stroke.Transparency = 0.65
	stroke.Thickness = 1
	stroke.Parent = f
	return f
end

local function label(parent, text, size, position, font, textSize, colour)
	local l = Instance.new("TextLabel")
	l.Text = text
	l.Size = size
	l.Position = position
	l.BackgroundTransparency = 1
	l.Font = font or Enum.Font.Gotham
	l.TextSize = textSize or 14
	l.TextColor3 = colour or Color3.fromRGB(232, 234, 238)
	l.TextXAlignment = Enum.TextXAlignment.Left
	l.TextYAlignment = Enum.TextYAlignment.Top
	l.Parent = parent
	return l
end

-- header
local header = panel(gui, UDim2.fromOffset(300, 92), UDim2.fromOffset(16, 16))
local _title = label(header, "WINTERLICHTPLATZ", UDim2.new(1, -20, 0, 22), UDim2.fromOffset(12, 10),
	Enum.Font.GothamBold, 17, Color3.fromRGB(246, 240, 226))
local _subtitle = label(header, "10 buildings · 35 floors · 176 rooms · 64 residents",
	UDim2.new(1, -20, 0, 16), UDim2.fromOffset(12, 34), Enum.Font.Gotham, 12,
	Color3.fromRGB(168, 176, 190))
local clockLabel = label(header, "15:36", UDim2.new(1, -20, 0, 20), UDim2.fromOffset(12, 56),
	Enum.Font.GothamMedium, 15, Color3.fromRGB(255, 216, 148))

-- quest panel
local quest = panel(gui, UDim2.fromOffset(320, 168), UDim2.fromOffset(16, 120))
local _questTitle = label(quest, "THE VERGER'S ERRAND", UDim2.new(1, -20, 0, 18), UDim2.fromOffset(12, 10),
	Enum.Font.GothamBold, 13, Color3.fromRGB(198, 206, 220))
local questHint = label(quest, "Find the Town Crier by the notice board and ask about the errands.",
	UDim2.new(1, -24, 0, 40), UDim2.fromOffset(12, 32), Enum.Font.Gotham, 12,
	Color3.fromRGB(150, 158, 172))
questHint.TextWrapped = true
local rows = {}
for i = 1, 3 do
	local row = label(quest, "", UDim2.new(1, -24, 0, 22), UDim2.fromOffset(12, 40 + (i - 1) * 30),
		Enum.Font.GothamMedium, 12, Color3.fromRGB(226, 228, 234))
	row.TextWrapped = true
	rows[i] = row
end
local progress = label(quest, "", UDim2.new(1, -24, 0, 20), UDim2.fromOffset(12, 140),
	Enum.Font.Gotham, 12, Color3.fromRGB(255, 216, 148))

-- footer hints
local footer = label(gui, "WASD walk · Space jump · climb the stairs inside any building · E to interact",
	UDim2.new(0, 520, 0, 20), UDim2.new(0.5, -260, 1, -32), Enum.Font.Gotham, 12,
	Color3.fromRGB(206, 210, 220))
footer.TextXAlignment = Enum.TextXAlignment.Center

-- toast
local toast = panel(gui, UDim2.fromOffset(420, 54), UDim2.new(0.5, -210, 0, 120))
toast.BackgroundColor3 = Color3.fromRGB(30, 26, 18)
toast.BackgroundTransparency = 0.1
local toastLabel = label(toast, "", UDim2.new(1, -24, 1, -12), UDim2.fromOffset(12, 8),
	Enum.Font.GothamMedium, 13, Color3.fromRGB(255, 226, 168))
toastLabel.TextWrapped = true
toast.Visible = false

local state = { errands = {}, total = 0, done = 0, active = false, completed = 0 }

local function showToast(text: string)
	toastLabel.Text = text
	toast.Visible = true
	toast.BackgroundTransparency = 0.1
	task.delay(5, function()
		TweenService:Create(toast, TweenInfo.new(0.6), { BackgroundTransparency = 1 }):Play()
		task.wait(0.6)
		toast.Visible = false
	end)
end

local function render()
	if not state.active and #state.errands == 0 then
		questHint.Text = "Find the Town Crier by the notice board and ask about the errands."
	else
		questHint.Text = "Parcels to deliver. Each one is on an upper floor: use the stairs."
	end
	for i = 1, 3 do
		local errand = state.errands[i]
		if errand then
			local tick = if errand.done then "[x]" else "[ ]"
			local dist = ""
			local char = player.Character
			local hrp = char and char:FindFirstChild("HumanoidRootPart")
			if hrp and errand.position and not errand.done then
				local target = Vector3.new(errand.position[1], errand.position[2], errand.position[3])
				dist = string.format("  ·  %dm", math.floor((hrp.Position - target).Magnitude))
			end
			rows[i].Text = string.format("%s %s, floor %d — %s%s", tick, errand.building, errand.floor, errand.label, dist)
			rows[i].TextColor3 = if errand.done
				then Color3.fromRGB(132, 186, 140)
				else Color3.fromRGB(226, 228, 234)
		else
			rows[i].Text = ""
		end
	end
	if state.total > 0 then
		progress.Text = string.format("%d of %d delivered · %d run(s) complete", state.done, state.total, state.completed)
	else
		progress.Text = ""
	end
end

questEvent.OnClientEvent:Connect(function(payload)
	if payload.kind == "state" then
		state.errands = payload.errands or {}
		state.total = payload.total or 0
		state.done = payload.done or 0
		state.active = payload.active and true or false
		state.completed = payload.completed or 0
		render()
	elseif payload.kind == "clock" then
		local h = math.floor(payload.clock)
		local m = math.floor((payload.clock - h) * 60)
		clockLabel.Text = string.format("%02d:%02d · %s · %d residents about",
			h, m,
			if payload.night then "lamps lit" else "daylight",
			payload.residents or 0)
	elseif payload.kind == "message" then
		showToast(payload.text)
	end
end)

task.spawn(function()
	while true do
		if #state.errands > 0 then
			render()
		end
		task.wait(0.5)
	end
end)

render()
