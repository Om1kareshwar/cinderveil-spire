extends Node

signal hp_changed(new_hp: int, max_hp: int)
signal embers_changed(count: int)
signal player_died
signal victory_achieved

var max_health: int = 5
var current_health: int = 5
var ember_count: int = 0
var total_embers_in_level: int = 0
var is_game_over: bool = false
var is_victory: bool = false

func _enter_tree() -> void:
	setup_default_inputs()

func _ready() -> void:
	reset_run()

func setup_default_inputs() -> void:
	var key_mappings = {
		"move_left": [KEY_A, KEY_LEFT],
		"move_right": [KEY_D, KEY_RIGHT],
		"jump": [KEY_SPACE, KEY_W, KEY_UP],
		"attack": [KEY_J],
		"restart": [KEY_R]
	}
	
	for action in key_mappings:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for keycode in key_mappings[action]:
			var event = InputEventKey.new()
			event.physical_keycode = keycode
			InputMap.action_add_event(action, event)
			
	if InputMap.has_action("attack"):
		var mouse_event = InputEventMouseButton.new()
		mouse_event.button_index = MOUSE_BUTTON_LEFT
		InputMap.action_add_event("attack", mouse_event)

func reset_run() -> void:
	current_health = max_health
	ember_count = 0
	is_game_over = false
	is_victory = false
	SoundManager.restart_bgm()
	emit_signal("hp_changed", current_health, max_health)
	emit_signal("embers_changed", ember_count)

func damage_player(amount: int) -> void:
	if is_game_over or is_victory:
		return
	current_health = max(0, current_health - amount)
	emit_signal("hp_changed", current_health, max_health)
	
	if current_health <= 0:
		is_game_over = true
		emit_signal("player_died")
		SoundManager.play_game_over_theme()
	else:
		SoundManager.play_heart_lost()

func heal_player(amount: int) -> void:
	current_health = min(max_health, current_health + amount)
	emit_signal("hp_changed", current_health, max_health)

func add_ember(amount: int = 1) -> void:
	ember_count += amount
	emit_signal("embers_changed", ember_count)

func trigger_victory() -> void:
	if is_game_over or is_victory:
		return
	is_victory = true
	emit_signal("victory_achieved")
