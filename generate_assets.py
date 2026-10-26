import os
import math
import struct
import zlib
import wave

OUTPUT_DIR = r"C:\Users\omkar\Desktop\cinderveil-spire"
SPRITES_DIR = os.path.join(OUTPUT_DIR, "assets", "sprites")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "assets", "audio")

os.makedirs(SPRITES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ----------------- PNG WRITER -----------------
def write_png(filename, width, height, rgba_data):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter type 0 (None)
        raw.extend(rgba_data[y * width * 4 : (y + 1) * width * 4])
    idat = zlib.compress(bytes(raw), level=6)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')
    with open(filename, 'wb') as f:
        f.write(png)

class Canvas:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = bytearray(w * h * 4)

    def set_pixel(self, x, y, r, g, b, a=255):
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 4
            self.data[idx] = r
            self.data[idx+1] = g
            self.data[idx+2] = b
            self.data[idx+3] = a

    def fill_rect(self, x, y, w, h, r, g, b, a=255):
        for cy in range(max(0, y), min(self.h, y + h)):
            for cx in range(max(0, x), min(self.w, x + w)):
                self.set_pixel(cx, cy, r, g, b, a)

    def save(self, filepath):
        write_png(filepath, self.w, self.h, self.data)

# Palette
C_VOID     = (13, 15, 27)
C_SLATE    = (24, 27, 44)
C_INDIGO   = (42, 45, 74)
C_STONE    = (67, 72, 107)
C_BASALT   = (104, 111, 153)
C_GREY     = (157, 164, 196)
C_SILVER   = (224, 230, 248)
C_MAROON   = (69, 22, 36)
C_CRIMSON  = (132, 30, 51)
C_EMBER    = (201, 59, 43)
C_ORANGE   = (232, 106, 35)
C_GOLD     = (244, 180, 54)
C_YELLOW   = (255, 232, 105)
C_CYAN     = (82, 214, 182)
C_WHITE    = (255, 255, 255)
C_BLACK    = (0, 0, 0)
C_MOSS     = (45, 106, 79)
C_LEAF     = (82, 183, 136)

# ----------------- 1. PLAYER SPRITESHEET (256 x 128) -----------------
# 8 frames per row, 4 rows, 32x32 per frame
def generate_player():
    c = Canvas(256, 128)
    
    # Helper to draw character base at frame (fx, fy)
    def draw_player_base(fx, fy, bob=0, leg_offset=0, eye_dir=0):
        ox = fx * 32
        oy = fy * 32
        
        # Cloak / Torso (center around x=14, y=14)
        c.fill_rect(ox + 12, oy + 12 + bob, 8, 11, *C_INDIGO)
        c.fill_rect(ox + 13, oy + 13 + bob, 6, 9, *C_SLATE)
        
        # Hood / Head
        c.fill_rect(ox + 11, oy + 6 + bob, 10, 8, *C_SLATE)
        c.fill_rect(ox + 12, oy + 5 + bob, 8, 8, *C_INDIGO)
        c.fill_rect(ox + 13, oy + 7 + bob, 7, 5, *C_VOID) # Face shadow
        # Glowing eye
        c.fill_rect(ox + 16 + eye_dir, oy + 8 + bob, 3, 2, *C_CYAN)
        c.fill_rect(ox + 17 + eye_dir, oy + 8 + bob, 1, 1, *C_WHITE)
        
        # Legs / Boots
        c.fill_rect(ox + 12 + leg_offset, oy + 23, 3, 5, *C_STONE)
        c.fill_rect(ox + 17 - leg_offset, oy + 23, 3, 5, *C_STONE)
        c.fill_rect(ox + 12 + leg_offset, oy + 26, 4, 3, *C_VOID)
        c.fill_rect(ox + 17 - leg_offset, oy + 26, 4, 3, *C_VOID)

    # Row 0: Frames 0..3: Idle
    for i in range(4):
        bob = 1 if (i == 1 or i == 2) else 0
        draw_player_base(i, 0, bob=bob)
        # Sword on back / side
        ox = i * 32
        c.fill_rect(ox + 8, 12 + bob, 2, 10, *C_SILVER)
        c.fill_rect(ox + 7, 10 + bob, 4, 2, *C_GOLD)
        c.fill_rect(ox + 8, 8 + bob, 2, 2, *C_CRIMSON)

    # Row 0: Frames 4..7: Jump & Fall
    # 4: Jump takeoff (squash)
    draw_player_base(4, 0, bob=2)
    # 5: Jump rising (stretch)
    draw_player_base(5, 0, bob=-2, leg_offset=1)
    # 6: Jump apex
    draw_player_base(6, 0, bob=-1)
    # 7: Falling
    draw_player_base(7, 0, bob=0, leg_offset=-1)

    # Row 1: Frames 0..5: Run
    run_leg_offsets = [2, 1, -1, -2, -1, 1]
    run_bobs = [0, 1, 0, 0, 1, 0]
    for i in range(6):
        draw_player_base(i, 1, bob=run_bobs[i], leg_offset=run_leg_offsets[i], eye_dir=1)
        ox = i * 32
        oy = 32
        # Flowing scarf / cape trail
        c.fill_rect(ox + 8 - run_leg_offsets[i], oy + 12 + run_bobs[i], 4, 3, *C_CRIMSON)
        c.fill_rect(ox + 6 - run_leg_offsets[i], oy + 14 + run_bobs[i], 3, 2, *C_MAROON)

    # Row 2: Frames 0..3: Attack combo
    # Frame 0: Windup
    draw_player_base(0, 2, bob=0)
    c.fill_rect(0 * 32 + 6, 64 + 10, 4, 12, *C_SILVER) # sword raised behind
    c.fill_rect(0 * 32 + 7, 64 + 8, 2, 3, *C_GOLD)

    # Frame 1: Slash Strike (Wide slash arc!)
    draw_player_base(1, 2, bob=1, eye_dir=1)
    ox = 1 * 32
    oy = 64
    # Fiery blade slashing forward
    c.fill_rect(ox + 18, oy + 14, 10, 3, *C_SILVER)
    # Slash crescent
    for a in range(8):
        c.fill_rect(ox + 20 + int(math.sin(a*0.4)*7), oy + 6 + a*2, 3, 2, *C_YELLOW)
        c.fill_rect(ox + 22 + int(math.sin(a*0.4)*6), oy + 5 + a*2, 2, 2, *C_ORANGE)
        c.fill_rect(ox + 24 + int(math.sin(a*0.4)*5), oy + 4 + a*2, 2, 2, *C_EMBER)

    # Frame 2: Slash follow-through
    draw_player_base(2, 2, bob=1, eye_dir=1)
    ox = 2 * 32
    oy = 64
    c.fill_rect(ox + 22, oy + 20, 8, 2, *C_SILVER)

    # Frame 3: Sheathe / Recovery
    draw_player_base(3, 2, bob=0)
    c.fill_rect(3 * 32 + 10, 64 + 16, 3, 8, *C_SILVER)

    # Row 2: Frames 4..5: Hurt (Recoil + Flash)
    # Frame 4: White flash
    ox = 4 * 32
    oy = 64
    c.fill_rect(ox + 10, oy + 6, 12, 22, *C_WHITE)
    # Frame 5: Red damage recoil
    draw_player_base(5, 2, bob=1, leg_offset=-2, eye_dir=-1)
    c.fill_rect(5 * 32 + 11, oy + 6, 10, 20, 255, 50, 50, 140)

    # Row 2: Frames 6..7: Death dissolve
    ox = 6 * 32
    oy = 64
    c.fill_rect(ox + 10, oy + 16, 12, 12, *C_CRIMSON)
    c.fill_rect(ox + 14, oy + 8, 4, 4, *C_EMBER)
    ox = 7 * 32
    c.fill_rect(ox + 8, oy + 24, 16, 5, *C_VOID)
    c.fill_rect(ox + 12, oy + 20, 8, 4, *C_CRIMSON)
    c.fill_rect(ox + 14, oy + 12, 3, 3, *C_GOLD)

    # Row 3: UI Icons (Hearts, Ember, Portal)
    # Frame 0: Full Heart
    ox = 0 * 32
    oy = 96
    heart_pixels = [
        (4, 2), (5, 2), (7, 2), (8, 2),
        (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
        (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
        (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
        (5, 6), (6, 6), (7, 6),
        (6, 7)
    ]
    for px, py in heart_pixels:
        c.set_pixel(ox + px * 2, oy + py * 2, *C_CRIMSON)
        c.set_pixel(ox + px * 2 + 1, oy + py * 2, *C_CRIMSON)
        c.set_pixel(ox + px * 2, oy + py * 2 + 1, *C_CRIMSON)
        c.set_pixel(ox + px * 2 + 1, oy + py * 2 + 1, *C_CRIMSON)
    # Heart highlight
    c.fill_rect(ox + 8, oy + 6, 2, 2, *C_YELLOW)

    # Frame 1: Empty Heart
    ox = 1 * 32
    oy = 96
    for px, py in [(4,2),(5,2),(7,2),(8,2),(3,3),(9,3),(3,4),(9,4),(4,5),(8,5),(5,6),(7,6),(6,7)]:
        c.fill_rect(ox + px * 2, oy + py * 2, 2, 2, *C_STONE)

    # Frame 2: Ember Flame
    ox = 2 * 32
    oy = 96
    for i in range(16):
        c.fill_rect(ox + 12, oy + 10, 8, 12, *C_EMBER)
        c.fill_rect(ox + 13, oy + 8, 6, 12, *C_ORANGE)
        c.fill_rect(ox + 14, oy + 10, 4, 8, *C_YELLOW)
        c.fill_rect(ox + 15, oy + 12, 2, 4, *C_WHITE)

    c.save(os.path.join(SPRITES_DIR, "player.png"))
    print("player.png generated.")

# ----------------- 2. ENEMY SPRITESHEET (256 x 64) -----------------
def generate_enemy():
    c = Canvas(256, 64)
    
    def draw_skeleton(fx, fy, step=0):
        ox = fx * 32
        oy = fy * 32
        
        # Skull
        c.fill_rect(ox + 12, oy + 6 + (step % 2), 8, 8, *C_SILVER)
        c.fill_rect(ox + 13, oy + 12 + (step % 2), 6, 2, *C_GREY) # teeth
        # Eye sockets
        c.set_pixel(ox + 14, oy + 9 + (step % 2), *C_CRIMSON)
        c.set_pixel(ox + 17, oy + 9 + (step % 2), *C_CRIMSON)
        
        # Spine & Ribcage
        c.fill_rect(ox + 13, oy + 14, 6, 6, *C_GREY)
        c.fill_rect(ox + 12, oy + 15, 8, 2, *C_SILVER)
        c.fill_rect(ox + 12, oy + 18, 8, 2, *C_SILVER)
        
        # Pelvis & Legs
        c.fill_rect(ox + 13, oy + 20, 6, 2, *C_GREY)
        lo = 2 if step == 1 else (-2 if step == 3 else 0)
        c.fill_rect(ox + 13 + lo, oy + 22, 2, 6, *C_SILVER)
        c.fill_rect(ox + 17 - lo, oy + 22, 2, 6, *C_SILVER)
        
        # Rusty Cleaver
        c.fill_rect(ox + 21, oy + 14 + (step % 2), 2, 10, *C_STONE)
        c.fill_rect(ox + 21, oy + 12 + (step % 2), 5, 8, *C_MAROON)

    # Row 0: Walk 4 frames
    for i in range(4):
        draw_skeleton(i, 0, step=i)

    # Frame 4..5: Attack swing
    draw_skeleton(4, 0, step=0)
    # Raised cleaver
    c.fill_rect(4 * 32 + 18, 4, 3, 10, *C_CRIMSON)
    c.fill_rect(4 * 32 + 17, 2, 6, 6, *C_EMBER)

    draw_skeleton(5, 0, step=1)
    # Downward cleave
    c.fill_rect(5 * 32 + 22, 18, 8, 4, *C_EMBER)
    c.fill_rect(5 * 32 + 20, 16, 4, 8, *C_ORANGE)

    # Frame 6: Hurt
    ox = 6 * 32
    c.fill_rect(ox + 10, 6, 12, 22, *C_WHITE)

    # Frame 7: Collapse / Dead
    ox = 7 * 32
    c.fill_rect(ox + 8, 24, 16, 6, *C_GREY)
    c.fill_rect(ox + 12, 20, 6, 6, *C_SILVER) # loose skull
    c.set_pixel(ox + 14, 22, *C_VOID)
    c.set_pixel(ox + 16, 22, *C_VOID)

    c.save(os.path.join(SPRITES_DIR, "enemy.png"))
    print("enemy.png generated.")

# ----------------- 3. TILESET (128 x 128) -----------------
def generate_tileset():
    c = Canvas(128, 128)
    
    # Tile (0,0): Deep Solid Crypt Brick (16x16)
    for y in range(16):
        for x in range(16):
            base = C_STONE if (x % 8 != 0 and y % 8 != 0) else C_SLATE
            c.set_pixel(x, y, *base)
    # Mortar highlights
    c.fill_rect(1, 1, 6, 1, *C_BASALT)
    c.fill_rect(9, 1, 6, 1, *C_BASALT)
    c.fill_rect(1, 9, 6, 1, *C_BASALT)

    # Tile (1,0): Top Ground with Moss / Grass edge
    ox = 16
    for y in range(16):
        for x in range(16):
            if y < 3:
                c.set_pixel(ox + x, y, *C_MOSS)
            elif y == 3:
                c.set_pixel(ox + x, y, *C_LEAF if x % 2 == 0 else C_MOSS)
            else:
                base = C_STONE if (x % 8 != 0 and y % 8 != 0) else C_SLATE
                c.set_pixel(ox + x, y, *base)

    # Tile (2,0): Left Edge Stone
    ox = 32
    for y in range(16):
        for x in range(16):
            if x < 3:
                c.set_pixel(ox + x, y, *C_SLATE)
            else:
                c.set_pixel(ox + x, y, *C_STONE)
    c.fill_rect(ox + 3, 1, 1, 14, *C_BASALT)

    # Tile (3,0): Right Edge Stone
    ox = 48
    for y in range(16):
        for x in range(16):
            if x > 12:
                c.set_pixel(ox + x, y, *C_SLATE)
            else:
                c.set_pixel(ox + x, y, *C_STONE)

    # Tile (0,1): Wooden One-Way Platform
    oy = 16
    c.fill_rect(0, oy + 2, 16, 5, 115, 65, 35) # wood brown
    c.fill_rect(0, oy + 1, 16, 1, 165, 105, 55) # top rim
    c.fill_rect(0, oy + 7, 16, 1, 60, 30, 15) # under shadow
    c.fill_rect(3, oy + 2, 2, 5, 80, 40, 20)
    c.fill_rect(11, oy + 2, 2, 5, 80, 40, 20)

    # Tile (1,1): Hazard Spikes (16x16)
    ox = 16
    oy = 16
    # 3 sharp spike teeth
    for s in range(3):
        sx = ox + 2 + s * 5
        for h in range(8):
            w = 1 + h // 2
            c.fill_rect(sx - w // 2, oy + 14 - h, w, 1, *C_SILVER)
        c.set_pixel(sx, oy + 14 - 7, *C_CRIMSON) # blood tipped
    c.fill_rect(ox, oy + 14, 16, 2, *C_SLATE)

    # Tile (2,1): Torch / Lantern on wall
    ox = 32
    oy = 16
    c.fill_rect(ox + 6, oy + 8, 4, 6, *C_STONE)
    c.fill_rect(ox + 7, oy + 10, 2, 4, *C_SLATE)
    # Fire core
    c.fill_rect(ox + 6, oy + 4, 4, 5, *C_EMBER)
    c.fill_rect(ox + 7, oy + 3, 2, 4, *C_YELLOW)

    # Tile (3,1): Portal Arch Shrine (16x16)
    ox = 48
    oy = 16
    c.fill_rect(ox + 2, oy + 1, 12, 14, *C_INDIGO)
    c.fill_rect(ox + 4, oy + 3, 8, 12, *C_CYAN)
    c.fill_rect(ox + 6, oy + 5, 4, 10, *C_WHITE)

    c.save(os.path.join(SPRITES_DIR, "tileset.png"))
    print("tileset.png generated.")

# ----------------- 4. PARALLAX BACKGROUND (384 x 216) -----------------
def generate_background():
    c = Canvas(384, 216)
    
    # Sky gradient (void abyss to twilight indigo)
    for y in range(216):
        t = y / 216.0
        r = int(C_VOID[0] * (1 - t) + C_INDIGO[0] * t)
        g = int(C_VOID[1] * (1 - t) + C_INDIGO[1] * t)
        b = int(C_VOID[2] * (1 - t) + C_INDIGO[2] * t)
        for x in range(384):
            c.set_pixel(x, y, r, g, b)

    # Distant Stars
    for sx, sy in [(20,15),(75,30),(110,12),(160,40),(210,18),(280,25),(340,10),(370,35),(90,60),(240,55)]:
        c.set_pixel(sx, sy, *C_SILVER)
        c.set_pixel(sx+1, sy, *C_WHITE)

    # Glowing Moon (at x=300, y=40, radius 18)
    mx, my, mr = 300, 42, 18
    for y in range(my - mr, my + mr):
        for x in range(mx - mr, mx + mr):
            dist = math.sqrt((x - mx)**2 + (y - my)**2)
            if dist <= mr:
                c.set_pixel(x, y, *C_SILVER)
            elif dist <= mr + 3:
                c.set_pixel(x, y, 100, 120, 160, 90)

    # Distant Spire Silhouettes (y > 100)
    for x in range(384):
        # Multi-frequency skyline
        h = int(120 + 35 * math.sin(x * 0.02) + 20 * math.sin(x * 0.05))
        # Spire peaks at specific intervals
        if abs(x - 80) < 15:
            h -= (15 - abs(x - 80)) * 4
        if abs(x - 190) < 22:
            h -= (22 - abs(x - 190)) * 3
        if abs(x - 270) < 12:
            h -= (12 - abs(x - 270)) * 4
            
        for y in range(max(0, h), 216):
            c.set_pixel(x, y, *C_SLATE)

    # Midground Crypt Ruins (y > 155)
    for x in range(384):
        h = int(160 + 15 * math.sin(x * 0.04) + 8 * math.cos(x * 0.08))
        if abs(x - 140) < 8 or abs(x - 230) < 8 or abs(x - 330) < 8: # ruined pillars
            h -= 25
        for y in range(max(0, h), 216):
            c.set_pixel(x, y, *C_INDIGO)

    c.save(os.path.join(SPRITES_DIR, "parallax_bg.png"))
    print("parallax_bg.png generated.")

# ----------------- 5. CHIPTUNE AUDIO SYNTHESIZER -----------------
def generate_audio():
    sample_rate = 22050

    def write_wav(filename, samples):
        with wave.open(filename, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            raw = bytearray()
            for s in samples:
                val = max(-32767, min(32767, int(s)))
                raw.extend(struct.pack('<h', val))
            w.writeframes(raw)

    # 1. JUMP SFX: Rising square wave chirp
    jump_samples = []
    dur = 0.11
    n_jump = int(sample_rate * dur)
    for i in range(n_jump):
        t = i / float(sample_rate)
        freq = 240.0 + 550.0 * (t / dur) ** 0.8
        phase = (t * freq) % 1.0
        wave_val = 12000 if phase < 0.5 else -12000
        env = 1.0 - (t / dur)
        jump_samples.append(wave_val * env)
    write_wav(os.path.join(AUDIO_DIR, "jump.wav"), jump_samples)

    # 2. SLASH SFX: White noise whoosh with bandpass slide
    slash_samples = []
    dur = 0.12
    n_slash = int(sample_rate * dur)
    import random
    rng = random.Random(42)
    for i in range(n_slash):
        t = i / float(sample_rate)
        env = math.sin(t / dur * math.pi)
        noise = rng.uniform(-1.0, 1.0)
        # Apply pseudo lowpass
        freq = 2400.0 * (1.0 - t/dur) + 300.0
        val = noise * math.sin(2.0 * math.pi * freq * t) * 16000.0 * env
        slash_samples.append(val)
    write_wav(os.path.join(AUDIO_DIR, "slash.wav"), slash_samples)

    # 3. HIT SFX: Heavy square drop + burst
    hit_samples = []
    dur = 0.12
    n_hit = int(sample_rate * dur)
    for i in range(n_hit):
        t = i / float(sample_rate)
        env = math.exp(-t * 28.0)
        freq = 180.0 - 110.0 * (t / dur)
        sq = 14000 if ((t * freq) % 1.0) < 0.5 else -14000
        noise = rng.uniform(-1.0, 1.0) * 10000.0 if t < 0.04 else 0.0
        hit_samples.append((sq + noise) * env)
    write_wav(os.path.join(AUDIO_DIR, "hit.wav"), hit_samples)

    # 4. PICKUP SFX: 3-note arpeggio (C6, E6, G6)
    pickup_samples = []
    notes = [1046.5, 1318.5, 1567.9] # C6, E6, G6
    sub_dur = 0.04
    for note in notes:
        n_note = int(sample_rate * sub_dur)
        for i in range(n_note):
            t = i / float(sample_rate)
            phase = (t * note) % 1.0
            sq = 11000 if phase < 0.25 else -11000
            env = 1.0 - (t / sub_dur) * 0.4
            pickup_samples.append(sq * env)
    write_wav(os.path.join(AUDIO_DIR, "pickup.wav"), pickup_samples)

    # 5. FOOTSTEP SFX: Short low thud
    step_samples = []
    dur = 0.04
    n_step = int(sample_rate * dur)
    for i in range(n_step):
        t = i / float(sample_rate)
        env = 1.0 - t / dur
        noise = rng.uniform(-1.0, 1.0) * 4000.0
        thud = math.sin(2.0 * math.pi * 90.0 * t) * 7000.0
        step_samples.append((thud + noise) * env)
    write_wav(os.path.join(AUDIO_DIR, "footstep.wav"), step_samples)

    # 6. ENEMY DIE SFX: Low disintegration crunch
    die_samples = []
    dur = 0.28
    n_die = int(sample_rate * dur)
    for i in range(n_die):
        t = i / float(sample_rate)
        env = 1.0 - (t / dur) ** 0.6
        freq = 200.0 * (1.0 - t/dur) + 40.0
        sq = 12000 if ((t * freq) % 1.0) < 0.5 else -12000
        noise = rng.uniform(-1.0, 1.0) * 9000.0
        die_samples.append((sq + noise) * env)
    write_wav(os.path.join(AUDIO_DIR, "enemy_die.wav"), die_samples)

    # 7. RETRO BGM: 8-bar looping dark chiptune progression
    # D minor / D Dorian: Dm -> Bb -> C -> Am (Tempo 125 BPM)
    print("Synthesizing looping chiptune BGM...")
    bpm = 125.0
    beat_dur = 60.0 / bpm
    total_beats = 16 # 4 measures of 4/4
    total_dur = total_beats * beat_dur
    n_bgm = int(sample_rate * total_dur)
    bgm_samples = [0.0] * n_bgm

    # Chord progression roots (D2, Bb1, C2, A1)
    chords = [
        {"root": 73.42, "notes": [146.83, 174.61, 220.00, 293.66]}, # Dm
        {"root": 58.27, "notes": [116.54, 146.83, 174.61, 233.08]}, # Bb
        {"root": 65.41, "notes": [130.81, 164.81, 196.00, 261.63]}, # C
        {"root": 55.00, "notes": [110.00, 130.81, 164.81, 220.00]}, # Am
    ]

    for beat in range(total_beats):
        bar = beat // 4
        chord = chords[bar]
        start_t = beat * beat_dur
        start_idx = int(start_t * sample_rate)

        # 1. Bassline (Triangle on every beat)
        bass_freq = chord["root"]
        bass_n = int(beat_dur * 0.9 * sample_rate)
        for i in range(bass_n):
            if start_idx + i < n_bgm:
                t = i / float(sample_rate)
                env = math.exp(-t * 3.5)
                # Triangle wave
                tri = 4.0 * abs(((t * bass_freq) % 1.0) - 0.5) - 1.0
                bgm_samples[start_idx + i] += tri * 6000.0 * env

        # 2. Arpeggiator (16th notes: 4 notes per beat)
        sub_n = int(beat_dur / 4.0 * sample_rate)
        for sub in range(4):
            sub_idx = start_idx + sub * sub_n
            arp_freq = chord["notes"][(beat * 4 + sub) % 4]
            for i in range(int(sub_n * 0.8)):
                if sub_idx + i < n_bgm:
                    t = i / float(sample_rate)
                    env = 1.0 - (i / float(sub_n * 0.8))
                    sq = 3000 if ((t * arp_freq) % 1.0) < 0.25 else -3000
                    bgm_samples[sub_idx + i] += sq * env

        # 3. Noise Drum: Kick on beat 0,2; Snare on beat 1,3
        drum_n = int(0.08 * sample_rate)
        is_snare = (beat % 2 == 1)
        for i in range(drum_n):
            if start_idx + i < n_bgm:
                t = i / float(sample_rate)
                env = 1.0 - t / 0.08
                if is_snare:
                    noise = rng.uniform(-1.0, 1.0) * 4500.0 * env
                    bgm_samples[start_idx + i] += noise
                else:
                    k_freq = 120.0 * (1.0 - t/0.08) + 40.0
                    kick = math.sin(2.0 * math.pi * k_freq * t) * 6000.0 * env
                    bgm_samples[start_idx + i] += kick

    write_wav(os.path.join(AUDIO_DIR, "bgm.wav"), bgm_samples)
    print("bgm.wav generated.")

if __name__ == "__main__":
    generate_player()
    generate_enemy()
    generate_tileset()
    generate_background()
    generate_audio()
    print("All assets successfully built!")
