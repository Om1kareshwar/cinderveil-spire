class_name EnemySkeleton
extends CharacterBody2D

@export var max_health: int = 30
@export var patrol_speed: float = 38.0
@export var chase_speed: float = 65.0
@export var damage: int = 1

var current_health: int = 30
var direction: int = 1
var player_target: Player = null
var is_dead: bool = false
var anim_timer: float = 0.0
var anim_frame: int = 0

@onready var sprite: Sprite2D = $Sprite2D
@onready var floor_detector: RayCast2D = $FloorDetector
@onready var wall_detector: RayCast2D = $WallDetector
@onready var hitbox: Area2D = $Hitbox

func _ready() -> void:
	current_health = max_health
	if hitbox:
		hitbox.body_entered.connect(_on_hitbox_body_entered)

func _physics_process(delta: float) -> void:
	if is_dead:
		return

	if not is_on_floor():
		velocity.y += 900.0 * delta

	if player_target:
		chase_player()
	else:
		patrol()

	move_and_slide()
	update_animation(delta)

func patrol() -> void:
	if wall_detector and wall_detector.is_colliding():
		direction *= -1
		update_facing()
	elif floor_detector and not floor_detector.is_colliding():
		direction *= -1
		update_facing()

	velocity.x = direction * patrol_speed

func chase_player() -> void:
	var dir_to_player = sign(player_target.global_position.x - global_position.x)
	if dir_to_player != 0 and dir_to_player != direction:
		direction = int(dir_to_player)
		update_facing()
	velocity.x = direction * chase_speed

func update_facing() -> void:
	sprite.flip_h = (direction == -1)
	if wall_detector:
		wall_detector.target_position.x = 14 * direction
	if floor_detector:
		floor_detector.position.x = 10 * direction

func update_animation(delta: float) -> void:
	anim_timer += delta
	var speed_rate = 0.12 if player_target else 0.18
	if anim_timer >= speed_rate:
		anim_timer = 0.0
		anim_frame = (anim_frame + 1) % 4
	sprite.frame = anim_frame # Row 0: 0..3 walk

func take_damage(amount: int, knockback: Vector2 = Vector2.ZERO) -> void:
	if is_dead:
		return

	current_health -= amount
	velocity = knockback * 160.0
	sprite.frame = 6 # Hurt frame
	sprite.modulate = Color(4.0, 4.0, 4.0, 1.0)
	
	get_tree().create_timer(0.1).timeout.connect(func():
		sprite.modulate = Color.WHITE
	)

	if current_health <= 0:
		die()

func die() -> void:
	is_dead = true
	velocity = Vector2.ZERO
	sprite.frame = 7 # Dead frame
	SoundManager.play_sfx("enemy_die")
	
	# Spawn ember pickup
	var ember_scene = load("res://scenes/ember_pickup.tscn")
	if ember_scene:
		var ember = ember_scene.instantiate()
		ember.global_position = global_position
		get_parent().add_child(ember)

	# Fade out
	var tween = create_tween()
	tween.tween_property(sprite, "modulate:a", 0.0, 0.4)
	tween.tween_callback(queue_free)

func _on_hitbox_body_entered(body: Node2D) -> void:
	if is_dead:
		return
	if body is Player:
		var knock_dir = Vector2(direction, -0.5).normalized() * 160.0
		body.take_damage(damage, knock_dir)

func _on_detection_area_body_entered(body: Node2D) -> void:
	if body is Player:
		player_target = body

func _on_detection_area_body_exited(body: Node2D) -> void:
	if body == player_target:
		player_target = null
