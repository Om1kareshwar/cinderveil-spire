class_name HUD
extends CanvasLayer

@onready var hp_bar: ProgressBar = $TopLeft/HealthBar
@onready var coin_label: Label = $TopRight/CoinBox/Margin/HBox/CoinLabel
@onready var message_banner: Panel = $MessageBanner
@onready var title_label: Label = $MessageBanner/VBoxContainer/TitleLabel
@onready var subtitle_label: Label = $MessageBanner/VBoxContainer/SubtitleLabel

func _ready() -> void:
	GameManager.hp_changed.connect(_on_hp_changed)
	GameManager.embers_changed.connect(_on_coins_changed)
	GameManager.player_died.connect(_on_player_died)
	GameManager.victory_achieved.connect(_on_victory)

	message_banner.visible = false
	if hp_bar:
		hp_bar.max_value = GameManager.max_health
		hp_bar.value = GameManager.current_health
	_on_coins_changed(GameManager.ember_count)

func _unhandled_input(event: InputEvent) -> void:
	if (GameManager.is_game_over or GameManager.is_victory) and event.is_action_pressed("restart"):
		restart_game()

func restart_game() -> void:
	GameManager.reset_run()
	get_tree().reload_current_scene()

func _on_hp_changed(new_hp: int, max_hp: int) -> void:
	if hp_bar:
		hp_bar.max_value = max_hp
		var tween = create_tween()
		tween.tween_property(hp_bar, "value", float(new_hp), 0.2).set_trans(Tween.TRANS_QUAD)

func _on_coins_changed(count: int) -> void:
	if coin_label:
		# Format as 6-digit counter like screenshot (e.g. 001990)
		coin_label.text = "%06d" % (count * 100)

func _on_player_died() -> void:
	message_banner.visible = true
	title_label.text = "KNOCKED OUT!"
	title_label.modulate = Color(1.0, 0.3, 0.3)
	subtitle_label.text = "Dan has been defeated!\nPress [R] to Fight Again"

func _on_victory() -> void:
	message_banner.visible = true
	title_label.text = "VILLAGE SAVED!"
	title_label.modulate = Color(1.0, 0.85, 0.2)
	subtitle_label.text = "All enemies cleared!\nPress [R] to Replay"
