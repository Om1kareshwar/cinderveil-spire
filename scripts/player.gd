class_name Player
extends CharacterBody2D

# --- Kinematic Variables ---
@export var speed: float = 145.0
@export var acceleration: float = 1000.0
@export var friction: float = 1200.0

@export var jump_height: float = 48.0 # pixels
@export var time_to_jump_peak: float = 0.30 # seconds
@export var time_to_jump_fall: float = 0.24 # seconds
@export var coyote_duration: float = 0.12
@export var jump_buffer_duration: float = 0.14

# Jump gravity mathematics
@onready var jump_velocity: float = -((2.0 * jump_height) / time_to_jump_peak)
@onready var jump_gravity: float = ((2.0 * jump_height) / (time_to_jump_peak * time_to_jump_peak))
@onready var fall_gravity: float = ((2.0 * jump_height) / (time_to_jump_fall * time_to_jump_fall))

# --- Nodes ---
@onready var sprite: Sprite2D = $Sprite2D
@onready var attack_area: Area2D = $AttackArea
@onready var attack_collision: CollisionShape2D = $AttackArea/CollisionShape2D
var speech_bubble: Sprite2D

# --- State ---
enum State { IDLE, RUN, JUMP, FALL, ATTACK, HURT, DEAD }
var current_state: State = State.IDLE

var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
var facing_direction: int = 1
var is_invulnerable: bool = false
var anim_timer: float = 0.0
var anim_frame_idx: int = 0
var footstep_timer: float = 0.0
var attack_combo_idx: int = 0

func _ready() -> void:
	if attack_collision:
		attack_collision.disabled = true
	if attack_area:
		attack_area.body_entered.connect(_on_attack_body_entered)
	setup_speech_bubble()

func setup_speech_bubble() -> void:
	speech_bubble = Sprite2D.new()
	var at = AtlasTexture.new()
	at.atlas = load("res://assets/sprites/player.png")
	at.region = Rect2(0, 96, 32, 32)
	speech_bubble.texture = at
	speech_bubble.position = Vector2(0, -28)
	add_child(speech_bubble)

	# Bouncy pop-in animation
	speech_bubble.scale = Vector2.ZERO
	var tween = create_tween()
	tween.tween_property(speech_bubble, "scale", Vector2(1.2, 1.2), 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(speech_bubble, "scale", Vector2(1.0, 1.0), 0.1)
	# Dismiss after 3 seconds
	get_tree().create_timer(3.0).timeout.connect(dismiss_speech_bubble)

func dismiss_speech_bubble() -> void:
	if is_instance_valid(speech_bubble) and speech_bubble.scale.x > 0.0:
		var tween = create_tween()
		tween.tween_property(speech_bubble, "scale", Vector2.ZERO, 0.2)

func _physics_process(delta: float) -> void:
	if GameManager.is_game_over or GameManager.is_victory:
		apply_friction(delta)
		move_and_slide()
		return

	# Void death safety check: if player falls below the map
	if global_position.y > 230.0 and not GameManager.is_game_over:
		handle_void_fall()
		return

	update_timers(delta)
	apply_gravity(delta)

	match current_state:
		State.IDLE, State.RUN:
			handle_ground_movement(delta)
			check_jump()
		State.JUMP, State.FALL:
			handle_air_movement(delta)
			check_jump_cut()
		State.ATTACK:
			apply_friction(delta)
		State.HURT:
			apply_friction(delta)

	move_and_slide()
	update_state_machine()
	update_animations(delta)

func update_timers(delta: float) -> void:
	if is_on_floor():
		coyote_timer = coyote_duration
	else:
		coyote_timer = max(0.0, coyote_timer - delta)

	if Input.is_action_just_pressed("jump"):
		jump_buffer_timer = jump_buffer_duration
	else:
		jump_buffer_timer = max(0.0, jump_buffer_timer - delta)

func apply_gravity(delta: float) -> void:
	var gravity = jump_gravity if velocity.y < 0.0 else fall_gravity
	velocity.y += gravity * delta

func handle_ground_movement(delta: float) -> void:
	if Input.is_action_just_pressed("attack"):
		dismiss_speech_bubble()
		start_attack()
		return

	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0:
		velocity.x = move_toward(velocity.x, direction * speed, acceleration * delta)
		set_facing(int(direction))
		footstep_timer -= delta
		if footstep_timer <= 0.0:
			SoundManager.play_sfx("footstep")
			footstep_timer = 0.26
	else:
		apply_friction(delta)
		footstep_timer = 0.0

func handle_air_movement(delta: float) -> void:
	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0:
		velocity.x = move_toward(velocity.x, direction * speed, (acceleration * 0.75) * delta)
		set_facing(int(direction))
	else:
		velocity.x = move_toward(velocity.x, 0.0, (friction * 0.3) * delta)

func apply_friction(delta: float) -> void:
	velocity.x = move_toward(velocity.x, 0.0, friction * delta)

func check_jump() -> void:
	if jump_buffer_timer > 0.0 and coyote_timer > 0.0:
		velocity.y = jump_velocity
		jump_buffer_timer = 0.0
		coyote_timer = 0.0
		current_state = State.JUMP
		SoundManager.play_sfx("jump")
		dismiss_speech_bubble()

func check_jump_cut() -> void:
	if Input.is_action_just_released("jump") and velocity.y < (jump_velocity * 0.5):
		velocity.y = jump_velocity * 0.5

func set_facing(dir: int) -> void:
	if dir == 0 or dir == facing_direction:
		return
	facing_direction = dir
	sprite.flip_h = (facing_direction == -1)
	if attack_area:
		attack_area.scale.x = facing_direction

func start_attack() -> void:
	current_state = State.ATTACK
	attack_combo_idx = (attack_combo_idx + 1) % 2
	velocity.x = facing_direction * 50.0 # Punch forward lunge
	SoundManager.play_sfx("slash", 1.1)

	if attack_collision:
		attack_collision.disabled = false

	get_tree().create_timer(0.20).timeout.connect(func():
		if attack_collision:
			attack_collision.disabled = true
		if current_state == State.ATTACK:
			current_state = State.IDLE
	)

func _on_attack_body_entered(body: Node2D) -> void:
	if body is EnemySkeleton and current_state == State.ATTACK:
		var knock_dir = Vector2(facing_direction, -0.4).normalized()
		body.take_damage(15, knock_dir)
		SoundManager.play_sfx("hit")

func update_state_machine() -> void:
	if current_state == State.ATTACK or current_state == State.HURT or current_state == State.DEAD:
		return

	if is_on_floor():
		current_state = State.RUN if abs(velocity.x) > 8.0 else State.IDLE
	else:
		current_state = State.JUMP if velocity.y < 0.0 else State.FALL

func update_animations(delta: float) -> void:
	anim_timer += delta
	match current_state:
		State.IDLE:
			if anim_timer >= 0.16:
				anim_timer = 0.0
				anim_frame_idx = (anim_frame_idx + 1) % 4
			sprite.frame = anim_frame_idx
		State.RUN:
			if anim_timer >= 0.08:
				anim_timer = 0.0
				anim_frame_idx = (anim_frame_idx + 1) % 6
			sprite.frame = 8 + anim_frame_idx
		State.JUMP:
			sprite.frame = 5
		State.FALL:
			sprite.frame = 7
		State.ATTACK:
			# Alternating punch (17) and baton strike (18)
			sprite.frame = 17 if attack_combo_idx == 1 else 18
		State.HURT:
			sprite.frame = 20
		State.DEAD:
			sprite.frame = 23

func handle_void_fall() -> void:
	SoundManager.play_sfx("hit", 0.7)
	GameManager.damage_player(1)
	if GameManager.current_health > 0:
		velocity = Vector2.ZERO
		global_position = Vector2(45, 160)
		current_state = State.IDLE
		is_invulnerable = true
		sprite.modulate = Color(4.0, 1.0, 1.0, 1.0)
		get_tree().create_timer(0.5).timeout.connect(func():
			sprite.modulate = Color.WHITE
			is_invulnerable = false
		)
	else:
		current_state = State.DEAD
		velocity = Vector2.ZERO

func take_damage(amount: int, knockback: Vector2 = Vector2.ZERO) -> void:
	if is_invulnerable or GameManager.is_game_over:
		return

	is_invulnerable = true
	current_state = State.HURT
	velocity = knockback
	GameManager.damage_player(amount)
	SoundManager.play_sfx("hit", 0.8)

	sprite.modulate = Color(4.0, 1.0, 1.0, 1.0)
	get_tree().create_timer(0.3).timeout.connect(func():
		sprite.modulate = Color.WHITE
		if current_state == State.HURT:
			current_state = State.IDLE
	)
	get_tree().create_timer(0.8).timeout.connect(func():
		is_invulnerable = false
	)
