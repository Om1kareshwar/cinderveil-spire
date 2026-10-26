class_name CameraController
extends Camera2D

@export var target_node: Node2D
@export var smooth_speed: float = 8.0

var trauma: float = 0.0
var max_offset: Vector2 = Vector2(8, 6)

func _ready() -> void:
	# Keep camera within bounds of 384x216
	position_smoothing_enabled = false

func _process(delta: float) -> void:
	if target_node:
		var target_pos = target_node.global_position
		# Limit camera bounds
		target_pos.x = clamp(target_pos.x, 192.0, 960.0)
		target_pos.y = clamp(target_pos.y, 108.0, 320.0)
		global_position = global_position.lerp(target_pos, smooth_speed * delta)

	# Handle trauma screen shake
	if trauma > 0.0:
		trauma = max(0.0, trauma - delta * 1.5)
		var shake = trauma * trauma
		offset = Vector2(
			randf_range(-1.0, 1.0) * max_offset.x * shake,
			randf_range(-1.0, 1.0) * max_offset.y * shake
		)
	else:
		offset = Vector2.ZERO

func add_trauma(amount: float) -> void:
	trauma = min(1.0, trauma + amount)
