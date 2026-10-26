class_name Player
extends CharacterBody2D

# --- Kinematic Variables ---
@export var speed: float = 135.0
@export var acceleration: float = 950.0
@export var friction: float = 1100.0

@export var jump_height: float = 46.0 # pixels
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

func _ready() -> void:
	if attack_collision:
		attack_collision.disabled = true
	if attack_area:
		attack_area.body_entered.connect(_on_attack_body_entered)

func _physics_process(delta: float) -> void:
	if GameManager.is_game_over or GameManager.is_victory:
		apply_friction(delta)
		move_and_slide()
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
		start_attack()
		return

	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0:
		velocity.x = move_toward(velocity.x, direction * speed, acceleration * delta)
		set_facing(int(direction))
		# Footstep sound
		footstep_timer -= delta
		if footstep_timer <= 0.0:
			SoundManager.play_sfx("footstep")
			footstep_timer = 0.28
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
	velocity.x = facing_direction * 45.0 # Small lunge
	SoundManager.play_sfx("slash")
	
	if attack_collision:
		attack_collision.disabled = false
		
	# Attack duration
	get_tree().create_timer(0.22).timeout.connect(func():
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
			sprite.frame = anim_frame_idx # 0..3
		State.RUN:
			if anim_timer >= 0.09:
				anim_timer = 0.0
				anim_frame_idx = (anim_frame_idx + 1) % 6
			sprite.frame = 8 + anim_frame_idx # 8..13
		State.JUMP:
			sprite.frame = 5
		State.FALL:
			sprite.frame = 7
		State.ATTACK:
			sprite.frame = 17 # Slash frame
		State.HURT:
			sprite.frame = 20 # Hurt frame
		State.DEAD:
			sprite.frame = 23 # Dead frame

func take_damage(amount: int, knockback: Vector2 = Vector2.ZERO) -> void:
	if is_invulnerable or GameManager.is_game_over:
		return

	is_invulnerable = true
	current_state = State.HURT
	velocity = knockback
	GameManager.damage_player(amount)
	SoundManager.play_sfx("hit", 0.8)

	# White damage flash
	sprite.modulate = Color(4.0, 1.0, 1.0, 1.0)
	
	# Invulnerability timer
	get_tree().create_timer(0.3).timeout.connect(func():
		sprite.modulate = Color.WHITE
		if current_state == State.HURT:
			current_state = State.IDLE
	)
	get_tree().create_timer(0.8).timeout.connect(func():
		is_invulnerable = false
	)
