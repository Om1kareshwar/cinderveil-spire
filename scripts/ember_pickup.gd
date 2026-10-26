class_name EmberPickup
extends Area2D

var base_y: float
var time_passed: float = 0.0
var is_collected: bool = false

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	base_y = position.y
	time_passed = randf() * 5.0
	body_entered.connect(_on_body_entered)

func _process(delta: float) -> void:
	if is_collected:
		return
	time_passed += delta
	# Floating bob
	position.y = base_y + sin(time_passed * 4.0) * 3.0

func _on_body_entered(body: Node2D) -> void:
	if is_collected:
		return
	if body is Player:
		is_collected = true
		SoundManager.play_sfx("pickup")
		GameManager.add_ember(1)
		
		# Collect float up & fade tween
		var tween = create_tween()
		tween.tween_property(self, "position:y", position.y - 12.0, 0.2)
		tween.parallel().tween_property(self, "scale", Vector2(1.5, 1.5), 0.2)
		tween.parallel().tween_property(self, "modulate:a", 0.0, 0.2)
		tween.tween_callback(queue_free)
