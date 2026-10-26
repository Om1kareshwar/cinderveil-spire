extends Node

var sounds: Dictionary = {}
var bgm_player: AudioStreamPlayer

func _ready() -> void:
	load_audio_assets()
	setup_bgm()

func load_audio_assets() -> void:
	var sound_names = ["jump", "slash", "hit", "pickup", "footstep", "enemy_die"]
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
		# Enable loop on AudioStreamWAV if supported
		if bgm_stream is AudioStreamWAV:
			bgm_stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		bgm_player.stream = bgm_stream
		bgm_player.volume_db = -8.0
		bgm_player.play()

func play_sfx(sound_name: String, pitch_scale: float = 1.0) -> void:
	if not sounds.has(sound_name):
		return
	var player = AudioStreamPlayer.new()
	player.stream = sounds[sound_name]
	player.pitch_scale = pitch_scale + randf_range(-0.06, 0.06)
	player.volume_db = -2.0
	add_child(player)
	player.play()
	player.finished.connect(player.queue_free)
