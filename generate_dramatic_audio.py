import os
import math
import struct
import wave
import random

AUDIO_DIR = r"C:\Users\omkar\Desktop\cinderveil-spire\assets\audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

SAMPLE_RATE = 22050

def write_wav(filename, samples):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        raw = bytearray()
        for s in samples:
            val = max(-32767, min(32767, int(s)))
            raw.extend(struct.pack('<h', val))
        w.writeframes(raw)

# ----------------- 1. DRAMATIC DEFAULT SOUNDTRACK (136 BPM) -----------------
# Intense, cinematic dark action theme (D Minor / D Dorian: Dm -> Bb -> Gm -> A7)
def generate_dramatic_bgm():
    print("Generating dramatic default action soundtrack...")
    bpm = 136.0
    beat_dur = 60.0 / bpm
    total_beats = 16 # 4 measures of 4/4
    total_dur = total_beats * beat_dur
    n_samples = int(SAMPLE_RATE * total_dur)
    samples = [0.0] * n_samples
    rng = random.Random(101)

    # Dm (D, F, A) -> Bb (Bb, D, F) -> Gm (G, Bb, D) -> A7 (A, C#, E, G)
    chords = [
        {"root": 73.42,  "stabs": [293.66, 349.23, 440.00],        "lead": [587.33, 698.46, 880.00, 783.99]}, # Dm
        {"root": 58.27,  "stabs": [233.08, 293.66, 349.23],        "lead": [466.16, 587.33, 698.46, 587.33]}, # Bb
        {"root": 49.00,  "stabs": [196.00, 233.08, 293.66],        "lead": [392.00, 466.16, 587.33, 523.25]}, # Gm
        {"root": 55.00,  "stabs": [220.00, 277.18, 329.63, 392.00], "lead": [440.00, 554.37, 659.25, 587.33]}, # A7
    ]

    for beat in range(total_beats):
        bar = beat // 4
        chord = chords[bar]
        start_t = beat * beat_dur
        start_idx = int(start_t * SAMPLE_RATE)

        # 1. Heavy Driving Cinematic Percussion
        # Pounding bass drum on beat 0 and 2, snappy battle snare on 1 and 3
        is_snare = (beat % 2 == 1)
        drum_len = int(0.12 * SAMPLE_RATE)
        for i in range(drum_len):
            if start_idx + i < n_samples:
                t = i / float(SAMPLE_RATE)
                env = 1.0 - t / 0.12
                if is_snare:
                    noise = rng.uniform(-1.0, 1.0) * 7000.0 * env
                    samples[start_idx + i] += noise
                else:
                    freq = 160.0 * (1.0 - t/0.12) + 38.0
                    kick = math.sin(2.0 * math.pi * freq * t) * 9000.0 * env
                    samples[start_idx + i] += kick

        # 16th-note battle hi-hats
        sub_hat = int(beat_dur / 4.0 * SAMPLE_RATE)
        for h in range(4):
            h_idx = start_idx + h * sub_hat
            for i in range(int(0.025 * SAMPLE_RATE)):
                if h_idx + i < n_samples:
                    t = i / float(SAMPLE_RATE)
                    env = 1.0 - t / 0.025
                    samples[h_idx + i] += rng.uniform(-1.0, 1.0) * 2500.0 * env

        # 2. Intense Driving Bassline (16th-note chug)
        bass_f = chord["root"]
        for sub in range(4):
            sub_idx = start_idx + sub * sub_hat
            f_cur = bass_f * (2.0 if sub in [1, 3] else 1.0)
            for i in range(int(sub_hat * 0.8)):
                if sub_idx + i < n_samples:
                    t = i / float(SAMPLE_RATE)
                    env = math.exp(-t * 18.0)
                    sq = 5500 if ((t * f_cur) % 1.0) < 0.5 else -5500
                    samples[sub_idx + i] += sq * env

        # 3. Dramatic Minor Chord Stabs (on beats 0, 1.5, 2.5)
        stabs = chord["stabs"]
        for freq in stabs:
            stab_len = int(beat_dur * 0.7 * SAMPLE_RATE)
            for i in range(stab_len):
                if start_idx + i < n_samples:
                    t = i / float(SAMPLE_RATE)
                    env = math.exp(-t * 5.0)
                    saw = (2.0 * ((t * freq) % 1.0) - 1.0) * 1600.0 * env
                    samples[start_idx + i] += saw

        # 4. Dramatic Heroic Lead Melody (50% square with vibrato)
        lead_note = chord["lead"][beat % 4]
        lead_len = int(beat_dur * 0.88 * SAMPLE_RATE)
        for i in range(lead_len):
            if start_idx + i < n_samples:
                t = i / float(SAMPLE_RATE)
                vib = 1.0 + 0.015 * math.sin(2.0 * math.pi * 5.5 * t)
                f_vib = lead_note * vib
                env = 1.0 - (i / float(lead_len)) * 0.25
                phase = (t * f_vib) % 1.0
                sq = 4500 if phase < 0.5 else -4500
                samples[start_idx + i] += sq * env

    write_wav(os.path.join(AUDIO_DIR, "bgm.wav"), samples)
    print("bgm.wav (dramatic default soundtrack) written.")

# ----------------- 2. DRAMATIC "LOST A HEART" AUDIO SFX -----------------
# Jarring minor dissonance sting: high descending minor arpeggio + sub drop + impact crunch
def generate_heart_lost_sfx():
    print("Generating dramatic lost-a-heart SFX...")
    dur = 0.42
    n_samples = int(SAMPLE_RATE * dur)
    samples = []
    rng = random.Random(33)

    # Dramatic minor chord dissonance (F5, D5, Ab4, D4)
    sting_notes = [698.46, 587.33, 415.30, 293.66]

    for i in range(n_samples):
        t = i / float(SAMPLE_RATE)
        val = 0.0

        # Layer 1: Descending minor dissonance notes (rapid 4-note cascade)
        note_idx = min(3, int(t / (dur / 4.0)))
        f_note = sting_notes[note_idx]
        env_note = math.exp(-((t % (dur / 4.0)) * 12.0))
        val += (12000 if ((t * f_note) % 1.0) < 0.5 else -12000) * env_note

        # Layer 2: Deep menacing pitch-drop sub thud (220 Hz down to 45 Hz)
        f_sub = 220.0 * math.exp(-t * 6.0) + 45.0
        env_sub = math.exp(-t * 8.0)
        val += math.sin(2.0 * math.pi * f_sub * t) * 16000.0 * env_sub

        # Layer 3: Glass / Heart fracture transient burst (first 40ms)
        if t < 0.06:
            noise_env = 1.0 - (t / 0.06)
            val += rng.uniform(-1.0, 1.0) * 14000.0 * noise_env

        samples.append(val)

    write_wav(os.path.join(AUDIO_DIR, "heart_lost.wav"), samples)
    print("heart_lost.wav written.")

# ----------------- 3. DRAMATIC GAME OVER SOUNDTRACK -----------------
# 7.5 seconds somber, tragic chiptune funeral march / defeat theme (72 BPM)
def generate_game_over_theme():
    print("Generating dramatic Game Over soundtrack...")
    bpm = 72.0
    beat_dur = 60.0 / bpm
    total_beats = 9 # ~7.5 seconds
    total_dur = total_beats * beat_dur
    n_samples = int(SAMPLE_RATE * total_dur)
    samples = [0.0] * n_samples
    rng = random.Random(999)

    # Tragic progression:
    # Beat 0: Dm (root 73.42) - Melody D5 (587.33)
    # Beat 1: Bb (root 58.27) - Melody C#5 (554.37) (dramatic tension!)
    # Beat 2: Gm (root 49.00) - Melody Bb4 (466.16)
    # Beat 3: A7 (root 55.00) - Melody A4 (440.00)
    # Beat 4: Dm (root 73.42) - Melody F4 (349.23)
    # Beat 5: Gm (root 49.00) - Melody E4 (329.63)
    # Beat 6: A7 (root 55.00) - Melody C#4 (277.18)
    # Beat 7..8: Dm Low final bell toll - Melody D3 (146.83) + hollow silence
    melody_track = [
        {"root": 73.42, "freq": 587.33, "chord": [293.66, 349.23, 440.00]}, # Dm
        {"root": 58.27, "freq": 554.37, "chord": [233.08, 277.18, 349.23]}, # Bbm
        {"root": 49.00, "freq": 466.16, "chord": [196.00, 233.08, 293.66]}, # Gm
        {"root": 55.00, "freq": 440.00, "chord": [220.00, 277.18, 329.63]}, # A7
        {"root": 73.42, "freq": 349.23, "chord": [293.66, 349.23, 440.00]}, # Dm
        {"root": 49.00, "freq": 329.63, "chord": [196.00, 246.94, 293.66]}, # Em
        {"root": 55.00, "freq": 277.18, "chord": [220.00, 277.18, 329.63]}, # A7
        {"root": 36.71, "freq": 146.83, "chord": [146.83, 220.00, 293.66]}, # Final Dm toll
        {"root": 36.71, "freq": 146.83, "chord": [146.83, 220.00, 293.66]}, # Fade out
    ]

    for beat in range(total_beats):
        step = melody_track[beat]
        start_t = beat * beat_dur
        start_idx = int(start_t * SAMPLE_RATE)
        step_len = int(beat_dur * 0.95 * SAMPLE_RATE)

        # 1. Distant funeral drum / Timpani on downbeat
        timpani_len = int(0.4 * SAMPLE_RATE)
        for i in range(timpani_len):
            if start_idx + i < n_samples:
                t = i / float(SAMPLE_RATE)
                env = math.exp(-t * 5.0)
                freq = 90.0 * (1.0 - t/0.4) + 32.0
                boom = math.sin(2.0 * math.pi * freq * t) * 11000.0 * env
                noise = rng.uniform(-1.0, 1.0) * 1800.0 * env
                samples[start_idx + i] += boom + noise

        # 2. Somber low bass root (Triangle wave)
        bass_f = step["root"]
        for i in range(step_len):
            if start_idx + i < n_samples:
                t = i / float(SAMPLE_RATE)
                env = math.exp(-t * 2.2)
                tri = (4.0 * abs(((t * bass_f) % 1.0) - 0.5) - 1.0) * 7000.0 * env
                samples[start_idx + i] += tri

        # 3. Soft mourning string pad (chords)
        for cf in step["chord"]:
            for i in range(step_len):
                if start_idx + i < n_samples:
                    t = i / float(SAMPLE_RATE)
                    env = math.sin(i / float(step_len) * math.pi)
                    saw = (2.0 * ((t * cf) % 1.0) - 1.0) * 1200.0 * env
                    samples[start_idx + i] += saw

        # 4. Tragic mourning lead melody (music box / bell chiptune)
        lead_f = step["freq"]
        for i in range(step_len):
            if start_idx + i < n_samples:
                t = i / float(SAMPLE_RATE)
                # Slow gentle vibrato
                vib = 1.0 + 0.012 * math.sin(2.0 * math.pi * 4.0 * t) if t > 0.15 else 1.0
                env = math.exp(-t * 2.5) # bell decay
                sq = 8000 if ((t * lead_f * vib) % 1.0) < 0.25 else -8000
                samples[start_idx + i] += sq * env

    # Fade out last second
    fade_start = int((total_dur - 1.2) * SAMPLE_RATE)
    for i in range(fade_start, n_samples):
        fade = 1.0 - (i - fade_start) / float(n_samples - fade_start)
        samples[i] *= max(0.0, fade)

    write_wav(os.path.join(AUDIO_DIR, "game_over.wav"), samples)
    print("game_over.wav written.")

if __name__ == "__main__":
    generate_dramatic_bgm()
    generate_heart_lost_sfx()
    generate_game_over_theme()
    print("All dramatic audio tracks generated successfully!")
