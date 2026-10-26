class_name SpikesHazard
extends Area2D

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		var knock_dir = Vector2(0, -1).normalized() * 180.0
		body.take_damage(1, knock_dir)
