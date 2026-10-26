class_name HUD
extends CanvasLayer

@onready var hearts_container: HBoxContainer = $HeartsContainer
@onready var ember_label: Label = $EmberContainer/Label
@onready var message_banner: Panel = $MessageBanner
@onready var title_label: Label = $MessageBanner/VBoxContainer/TitleLabel
@onready var subtitle_label: Label = $MessageBanner/VBoxContainer/SubtitleLabel

var heart_textures: Array[TextureRect] = []

func _ready() -> void:
	GameManager.hp_changed.connect(_on_hp_changed)
	GameManager.embers_changed.connect(_on_embers_changed)
	GameManager.player_died.connect(_on_player_died)
	GameManager.victory_achieved.connect(_on_victory)

	message_banner.visible = false
	build_hearts(GameManager.max_health)
	_on_hp_changed(GameManager.current_health, GameManager.max_health)
	_on_embers_changed(GameManager.ember_count)

func _unhandled_input(event: InputEvent) -> void:
	if (GameManager.is_game_over or GameManager.is_victory) and event.is_action_pressed("restart"):
		restart_game()

func restart_game() -> void:
	GameManager.reset_run()
	get_tree().reload_current_scene()

func build_hearts(count: int) -> void:
	for child in hearts_container.get_children():
		child.queue_free()
	heart_textures.clear()

	# Create AtlasTexture referencing player.png Row 3, Frame 0 (Full Heart)
	var full_tex = AtlasTexture.new()
	full_tex.atlas = load("res://assets/sprites/player.png")
	full_tex.region = Rect2(0, 96, 32, 32)

	for i in range(count):
		var tr = TextureRect.new()
		tr.texture = full_tex
		tr.custom_minimum_size = Vector2(16, 16)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		hearts_container.add_child(tr)
		heart_textures.append(tr)

func _on_hp_changed(new_hp: int, _max_hp: int) -> void:
	var full_rect = Rect2(0, 96, 32, 32)
	var empty_rect = Rect2(32, 96, 32, 32)
	var atlas = load("res://assets/sprites/player.png")

	for i in range(heart_textures.size()):
		var at = AtlasTexture.new()
		at.atlas = atlas
		at.region = full_rect if (i < new_hp) else empty_rect
		heart_textures[i].texture = at

func _on_embers_changed(count: int) -> void:
	if ember_label:
		ember_label.text = "x %02d" % count

func _on_player_died() -> void:
	message_banner.visible = true
	title_label.text = "ASHES TO ASHES"
	title_label.modulate = Color(1.0, 0.3, 0.3)
	subtitle_label.text = "Your ember has faded.\nPress [R] to Kindle Anew"

func _on_victory() -> void:
	message_banner.visible = true
	title_label.text = "SPIRE CLEANSED!"
	title_label.modulate = Color(1.0, 0.85, 0.3)
	subtitle_label.text = "The Rift is sealed.\nPress [R] to Ascend Again"
