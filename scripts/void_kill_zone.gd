class_name VoidKillZone
extends Area2D

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		body.handle_void_fall()
	elif body is EnemySkeleton:
		body.queue_free()
