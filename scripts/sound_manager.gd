extends Node

var sounds: Dictionary = {}
var bgm_player: AudioStreamPlayer
var game_over_player: AudioStreamPlayer

func _ready() -> void:
	load_audio_assets()
	setup_bgm()
	setup_game_over()

func load_audio_assets() -> void:
	var sound_names = ["jump", "slash", "hit", "pickup", "footstep", "enemy_die", "heart_lost"]
	for s_name in sound_names:
		var path = "res://assets/audio/" + s_name + ".wav"
		if ResourceLoader.exists(path):
			var stream = load(path)
			sounds[s_name] = stream

func setup_bgm() -> void:
	bgm_player = AudioStreamPlayer.new()
	add_child(bgm_player)
	var bgm_path = "res://assets/audio/bgm.wav"
	if ResourceLoader.exists(bgm_path):
		var bgm_stream: AudioStream = load(bgm_path)
		if bgm_stream is AudioStreamWAV:
			bgm_stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		bgm_player.stream = bgm_stream
		bgm_player.volume_db = -6.0
		bgm_player.play()

func setup_game_over() -> void:
	game_over_player = AudioStreamPlayer.new()
	add_child(game_over_player)
	var go_path = "res://assets/audio/game_over.wav"
	if ResourceLoader.exists(go_path):
		var go_stream: AudioStream = load(go_path)
		game_over_player.stream = go_stream
		game_over_player.volume_db = -3.0

func play_sfx(sound_name: String, pitch_scale: float = 1.0) -> void:
	if not sounds.has(sound_name):
		return
	var player = AudioStreamPlayer.new()
	player.stream = sounds[sound_name]
	player.pitch_scale = pitch_scale + randf_range(-0.05, 0.05)
	player.volume_db = -2.0
	add_child(player)
	player.play()
	player.finished.connect(player.queue_free)

func play_heart_lost() -> void:
	play_sfx("heart_lost", 1.0)

func play_game_over_theme() -> void:
	if is_instance_valid(bgm_player):
		bgm_player.stop()
	if is_instance_valid(game_over_player):
		game_over_player.play()

func restart_bgm() -> void:
	if is_instance_valid(game_over_player):
		game_over_player.stop()
	if is_instance_valid(bgm_player) and not bgm_player.playing:
		bgm_player.play()
