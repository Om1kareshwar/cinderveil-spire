import os
import math
import struct
import zlib
import wave
import random

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
        raw.append(0)  # filter type 0
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

    def draw_outline_rect(self, x, y, w, h, r_in, g_in, b_in, r_out=0, g_out=0, b_out=0):
        # Fill inner
        self.fill_rect(x+1, y+1, w-2, h-2, r_in, g_in, b_in)
        # Outline
        for cx in range(x, x+w):
            self.set_pixel(cx, y, r_out, g_out, b_out)
            self.set_pixel(cx, y+h-1, r_out, g_out, b_out)
        for cy in range(y, y+h):
            self.set_pixel(x, cy, r_out, g_out, b_out)
            self.set_pixel(x+w-1, cy, r_out, g_out, b_out)

    def save(self, filepath):
        write_png(filepath, self.w, self.h, self.data)

# Palette based on uploaded screenshot
C_SKY_TOP   = (77, 166, 255)
C_SKY_BOT   = (153, 204, 255)
C_MNT_FAR   = (128, 179, 217)
C_MNT_MID   = (70, 130, 160)
C_PINES     = (45, 95, 115)
C_WHEAT_L   = (255, 215, 64)
C_WHEAT_M   = (230, 185, 30)
C_WHEAT_D   = (195, 145, 15)

C_GRASS_TOP = (56, 217, 78)
C_GRASS_MID = (40, 180, 56)
C_GRASS_DRK = (28, 135, 39)

C_DIRT_L    = (141, 110, 99)
C_DIRT_M    = (109, 76, 65)
C_DIRT_D    = (78, 52, 46)
C_DIRT_DARK = (46, 28, 22)

C_WOOD_L    = (180, 120, 60)
C_WOOD_M    = (140, 85, 35)
C_WOOD_D    = (85, 45, 18)

C_ROOF_L    = (78, 72, 102)
C_ROOF_M    = (52, 49, 76)
C_ROOF_D    = (35, 33, 50)

C_WHITE     = (255, 255, 255)
C_BLACK     = (20, 20, 25)
C_SKIN_L    = (254, 211, 166)
C_SKIN_M    = (226, 168, 117)
C_HAIR      = (30, 28, 35)

C_SUIT_RED  = (230, 46, 45)
C_SUIT_DRK  = (175, 25, 25)
C_GOLD_L    = (255, 235, 70)
C_GOLD_M    = (251, 192, 45)
C_GOLD_D    = (215, 145, 15)

# ----------------- 1. DAN THE BRAWLER PLAYER SPRITESHEET (256 x 128) -----------------
def generate_dan_player():
    c = Canvas(256, 128)
    
    def draw_dan(fx, fy, bob=0, leg_step=0, punch=0, facing=1, is_hurt=False):
        ox = fx * 32
        oy = fy * 32
        
        # Head (Blocky cartoon shape: 10x9)
        hx = ox + 11
        hy = oy + 7 + bob
        # Outline
        c.fill_rect(hx-1, hy-1, 12, 11, *C_BLACK)
        # Skin base
        c.fill_rect(hx, hy, 10, 9, *C_SKIN_L)
        c.fill_rect(hx+1, hy+6, 8, 3, *C_SKIN_M) # jaw shadow
        
        # Short spiky/side-part black hair
        c.fill_rect(hx-1, hy-1, 12, 4, *C_HAIR)
        c.fill_rect(hx, hy+3, 2, 2, *C_HAIR) # sideburn
        c.fill_rect(hx+3, hy-2, 3, 2, *C_HAIR) # front tuft
        
        # Eyes
        if is_hurt:
            # Comedic X eyes
            c.set_pixel(hx+3, hy+4, *C_BLACK)
            c.set_pixel(hx+5, hy+4, *C_BLACK)
            c.set_pixel(hx+4, hy+5, *C_BLACK)
            c.set_pixel(hx+7, hy+4, *C_BLACK)
            c.set_pixel(hx+9, hy+4, *C_BLACK)
            c.set_pixel(hx+8, hy+5, *C_BLACK)
        else:
            # Big white cartoon eyes with pupils
            c.fill_rect(hx+3, hy+3, 3, 4, *C_WHITE)
            c.fill_rect(hx+7, hy+3, 3, 4, *C_WHITE)
            c.fill_rect(hx+4, hy+4, 2, 3, *C_BLACK) # pupil
            c.fill_rect(hx+8, hy+4, 2, 3, *C_BLACK)
            # Determined mouth line
            c.fill_rect(hx+4, hy+7, 4, 1, *C_BLACK)

        # Torso (Black sleeveless combat shirt / vest: 10x8)
        tx = ox + 11
        ty = oy + 16 + bob
        c.fill_rect(tx-1, ty-1, 12, 10, *C_BLACK)
        c.fill_rect(tx, ty, 10, 8, 38, 38, 43) # dark tactical grey/black
        # Belt with silver buckle
        c.fill_rect(tx, ty+6, 10, 2, 60, 55, 50)
        c.fill_rect(tx+4, ty+6, 2, 2, 200, 200, 210) # buckle

        # Bare muscular arms / Fists
        if punch == 1:
            # Left arm holding stick / back
            c.fill_rect(tx-3, ty+1, 3, 4, *C_SKIN_L)
            # Right arm extended forward in a punch!
            c.fill_rect(tx+10, ty+1, 8, 4, *C_BLACK) # outline
            c.fill_rect(tx+10, ty+2, 7, 3, *C_SKIN_L)
            c.fill_rect(tx+15, ty+1, 4, 5, *C_BLACK) # fist outline
            c.fill_rect(tx+15, ty+2, 3, 3, *C_SKIN_M) # fist
            # Punch swoosh impact
            c.fill_rect(tx+19, ty, 3, 6, *C_WHITE)
            c.fill_rect(tx+22, ty+1, 2, 4, *C_GOLD_L)
        elif punch == 2:
            # Stick / baton swing!
            c.fill_rect(tx-2, ty+1, 3, 4, *C_SKIN_L)
            c.fill_rect(tx+8, ty, 6, 4, *C_SKIN_L)
            # Wooden baton club swung forward
            c.fill_rect(tx+12, ty-5, 3, 12, *C_BLACK)
            c.fill_rect(tx+13, ty-4, 2, 10, *C_WOOD_L)
            # Yellow comic action smear
            for a in range(6):
                c.fill_rect(tx+16 + a, ty - 3 + a, 2, 2, *C_GOLD_L)
        else:
            # Normal ready arms / holding club
            c.fill_rect(tx-3, ty+1, 3, 5, *C_SKIN_L)
            c.fill_rect(tx+10, ty+1, 3, 5, *C_SKIN_L)
            # Club in hand pointing up
            c.fill_rect(tx+11, ty-4, 3, 8, *C_BLACK)
            c.fill_rect(tx+12, ty-3, 2, 7, *C_WOOD_L)

        # Legs (Dark combat pants & boots)
        lx = ox + 11
        ly = oy + 24
        l_off = leg_step
        c.fill_rect(lx+1-l_off, ly, 3, 5, 50, 55, 65) # dark pants
        c.fill_rect(lx+6+l_off, ly, 3, 5, 50, 55, 65)
        # Black combat boots
        c.fill_rect(lx-l_off, ly+4, 4, 4, *C_BLACK)
        c.fill_rect(lx+6+l_off, ly+4, 4, 4, *C_BLACK)
        c.fill_rect(lx+1-l_off, ly+5, 3, 2, 60, 45, 35)
        c.fill_rect(lx+7+l_off, ly+5, 3, 2, 60, 45, 35)

    # Row 0: Idle (4 frames)
    for i in range(4):
        bob = 1 if (i == 1 or i == 2) else 0
        draw_dan(i, 0, bob=bob)

    # Row 0: Jump & Fall (4 frames)
    # 4: Jump takeoff crouch
    draw_dan(4, 0, bob=2)
    # 5: Jump soaring up (legs tucked)
    draw_dan(5, 0, bob=-2, leg_step=2)
    # 6: Apex
    draw_dan(6, 0, bob=-1, leg_step=1)
    # 7: Falling downward
    draw_dan(7, 0, bob=0, leg_step=-1)

    # Row 1: Run (6 frames - high knee comedic sprint!)
    run_steps = [2, 1, -1, -2, -1, 1]
    run_bobs  = [0, 1, 0, 0, 1, 0]
    for i in range(6):
        draw_dan(i, 1, bob=run_bobs[i], leg_step=run_steps[i])

    # Row 2: Attacks (Combo strikes)
    # Frame 0: Windup punch
    draw_dan(0, 2, bob=0, punch=0)
    # Frame 1: Power Punch!
    draw_dan(1, 2, bob=1, punch=1)
    # Frame 2: Baton Club Cleave!
    draw_dan(2, 2, bob=1, punch=2)
    # Frame 3: Recovery
    draw_dan(3, 2, bob=0, punch=0)

    # Frame 4..5: Hurt (Recoil + comic X eyes)
    draw_dan(4, 2, bob=1, is_hurt=True)
    # White damage flash
    ox = 5 * 32
    oy = 64
    c.fill_rect(ox+9, oy+6, 14, 22, *C_WHITE)

    # Frame 6..7: Knockout
    ox = 6 * 32
    oy = 64
    draw_dan(6, 2, bob=2, is_hurt=True)
    # Stars around head
    c.fill_rect(ox+8, oy+4, 2, 2, *C_GOLD_L)
    c.fill_rect(ox+22, oy+4, 2, 2, *C_GOLD_L)
    c.fill_rect(ox+15, oy+1, 2, 2, *C_GOLD_L)

    ox = 7 * 32
    # Knocked flat on ground
    c.fill_rect(ox+4, oy+22, 24, 7, *C_BLACK)
    c.fill_rect(ox+5, oy+23, 8, 5, *C_SKIN_L) # head
    c.fill_rect(ox+13, oy+23, 8, 5, 38, 38, 43) # body
    c.fill_rect(ox+21, oy+23, 6, 4, 50, 55, 65) # legs

    # Row 3: Comic Props & UI Icons (32x32 frames)
    # Frame 0: Comic Speech Bubble [ ! ]
    ox = 0 * 32
    oy = 96
    # White rounded balloon
    c.fill_rect(ox+6, oy+4, 20, 18, *C_BLACK)
    c.fill_rect(ox+7, oy+5, 18, 16, *C_WHITE)
    # Little tail pointing down
    c.fill_rect(ox+10, oy+22, 5, 4, *C_BLACK)
    c.fill_rect(ox+11, oy+21, 3, 3, *C_WHITE)
    # Bold black exclamation mark
    c.fill_rect(ox+14, oy+8, 4, 7, *C_BLACK)
    c.fill_rect(ox+14, oy+17, 4, 3, *C_BLACK)

    # Frame 1: Golden Coin with smiling face (as in screenshot)
    ox = 1 * 32
    oy = 96
    # Outer dark rim
    for cy in range(oy+4, oy+28):
        for cx in range(ox+4, ox+28):
            d = math.sqrt((cx - (ox+16))**2 + (cy - (oy+16))**2)
            if d <= 11.5:
                c.set_pixel(cx, cy, *C_BLACK)
            if d <= 10.0:
                c.set_pixel(cx, cy, *C_GOLD_M)
            if d <= 8.5:
                c.set_pixel(cx, cy, *C_GOLD_L)
    # Smiling eyes and mouth in coin
    c.fill_rect(ox+13, oy+13, 2, 3, *C_GOLD_D)
    c.fill_rect(ox+17, oy+13, 2, 3, *C_GOLD_D)
    c.fill_rect(ox+13, oy+18, 6, 2, *C_GOLD_D)
    c.fill_rect(ox+14, oy+19, 4, 1, *C_GOLD_D)

    # Frame 2: Red Health Potion (from screenshot)
    ox = 2 * 32
    oy = 96
    # Glass flask outline
    c.fill_rect(ox+10, oy+10, 12, 14, *C_BLACK)
    c.fill_rect(ox+13, oy+6, 6, 5, *C_BLACK) # neck
    # Cork
    c.fill_rect(ox+14, oy+5, 4, 2, *C_WOOD_L)
    # Red potion liquid
    c.fill_rect(ox+11, oy+13, 10, 10, *C_SUIT_RED)
    c.fill_rect(ox+12, oy+11, 8, 2, 255, 100, 100) # surface bubbles
    # Specular glass shine
    c.fill_rect(ox+12, oy+14, 2, 5, *C_WHITE)

    # Frame 3: Dragon Head Portrait Badge (for HUD)
    ox = 3 * 32
    oy = 96
    c.fill_rect(ox+6, oy+6, 20, 20, *C_BLACK)
    c.fill_rect(ox+7, oy+7, 18, 18, *C_SUIT_RED)
    # Dragon horns & muzzle
    c.fill_rect(ox+6, oy+4, 4, 4, *C_GOLD_L)
    c.fill_rect(ox+16, oy+10, 8, 8, *C_SUIT_RED)
    # Teeth
    c.fill_rect(ox+18, oy+14, 2, 3, *C_WHITE)
    c.fill_rect(ox+21, oy+14, 2, 3, *C_WHITE)
    # Dragon eye
    c.fill_rect(ox+12, oy+9, 4, 4, *C_WHITE)
    c.fill_rect(ox+13, oy+10, 2, 2, *C_BLACK)

    c.save(os.path.join(SPRITES_DIR, "player.png"))
    print("Dan player.png generated.")

# ----------------- 2. RED JETPACK NINJA & DRAGON ENEMIES (256 x 64) -----------------
def generate_dan_enemies():
    c = Canvas(256, 64)

    # Row 0: Red Jetpack Ninja (4 walk/fly frames + 2 attack + 2 hurt)
    def draw_ninja(fx, fy, thruster=0, shoot=False, is_hurt=False):
        ox = fx * 32
        oy = fy * 32
        
        # Jetpack on back
        c.fill_rect(ox+6, oy+13, 5, 10, *C_BLACK)
        c.fill_rect(ox+7, oy+14, 3, 8, 180, 180, 190)
        # Thruster exhaust flame
        if thruster > 0:
            c.fill_rect(ox+7, oy+23, 3, 3+thruster, *C_GOLD_L)
            c.fill_rect(ox+8, oy+24, 1, 3+thruster, *C_WHITE)
            # Smoke puff
            c.fill_rect(ox+5, oy+25+thruster, 7, 2, 220, 240, 255, 180)

        # Hooded Head (Red suit)
        c.fill_rect(ox+11, oy+7, 11, 10, *C_BLACK)
        c.fill_rect(ox+12, oy+8, 9, 8, *C_SUIT_RED)
        # White visor / Goggles (as in screenshot)
        if is_hurt:
            c.fill_rect(ox+13, oy+10, 7, 3, *C_WHITE)
            c.set_pixel(ox+14, oy+11, *C_BLACK)
            c.set_pixel(ox+18, oy+11, *C_BLACK)
        else:
            c.fill_rect(ox+13, oy+10, 7, 4, *C_WHITE)
            c.fill_rect(ox+15, oy+11, 3, 2, *C_BLACK) # eyes inside visor

        # Body (Red suit + straps)
        c.fill_rect(ox+11, oy+16, 11, 8, *C_BLACK)
        c.fill_rect(ox+12, oy+17, 9, 6, *C_SUIT_RED)
        c.fill_rect(ox+14, oy+17, 2, 6, *C_SUIT_DRK) # strap

        # Weapon
        if shoot:
            # Gun pointing forward
            c.fill_rect(ox+19, oy+17, 10, 3, *C_BLACK)
            c.fill_rect(ox+20, oy+18, 8, 1, 90, 90, 100)
            # Muzzle flash
            c.fill_rect(ox+28, oy+16, 3, 5, *C_GOLD_L)
            c.fill_rect(ox+29, oy+17, 1, 3, *C_WHITE)
        else:
            # Holding weapon at hip
            c.fill_rect(ox+18, oy+18, 7, 3, *C_BLACK)

        # Legs (Black boots)
        c.fill_rect(ox+12, oy+23, 4, 5, *C_BLACK)
        c.fill_rect(ox+17, oy+23, 4, 5, *C_BLACK)
        c.fill_rect(ox+13, oy+24, 2, 3, 70, 70, 80)
        c.fill_rect(ox+18, oy+24, 2, 3, 70, 70, 80)

    # 4 Walk/Fly frames
    for i in range(4):
        draw_ninja(i, 0, thruster=(i % 2) * 2)

    # 2 Attack/Shoot frames
    draw_ninja(4, 0, thruster=2, shoot=True)
    draw_ninja(5, 0, thruster=3, shoot=True)

    # 2 Hurt frames
    draw_ninja(6, 0, thruster=0, is_hurt=True)
    # White flash
    ox = 7 * 32
    c.fill_rect(ox+8, 7, 18, 22, *C_WHITE)

    # Row 1: Flying Red Dragon Mascot (from screenshot!)
    def draw_dragon(fx, fy, flap=0, is_hurt=False):
        ox = fx * 32
        oy = fy * 32
        
        # Dragon big head (16x14)
        c.fill_rect(ox+7, oy+5, 18, 16, *C_BLACK)
        c.fill_rect(ox+8, oy+6, 16, 14, *C_SUIT_RED)
        
        # Yellow horns & scales
        c.fill_rect(ox+7, oy+3, 4, 3, *C_GOLD_L)
        c.fill_rect(ox+12, oy+3, 3, 3, *C_GOLD_L)
        
        # Giant open cartoon jaw with teeth!
        c.fill_rect(ox+16, oy+10, 8, 8, *C_BLACK)
        c.fill_rect(ox+17, oy+11, 6, 6, 120, 20, 20) # mouth interior
        # Sharp white teeth
        c.fill_rect(ox+17, oy+11, 2, 2, *C_WHITE)
        c.fill_rect(ox+21, oy+11, 2, 2, *C_WHITE)
        c.fill_rect(ox+18, oy+15, 2, 2, *C_WHITE)
        
        # Big white eyes
        if is_hurt:
            c.fill_rect(ox+10, oy+8, 5, 4, *C_WHITE)
            c.set_pixel(ox+12, oy+9, *C_BLACK)
        else:
            c.fill_rect(ox+10, oy+7, 6, 5, *C_WHITE)
            c.fill_rect(ox+12, oy+8, 3, 3, *C_BLACK)
            c.set_pixel(ox+13, oy+8, *C_WHITE) # twinkle
            
        # Green dragon collar / underbelly
        c.fill_rect(ox+8, oy+20, 14, 5, 46, 204, 113) # bright green
        c.fill_rect(ox+9, oy+21, 12, 3, 39, 174, 96)
        
        # Flapping wings
        wing_y = oy + 10 + flap
        c.fill_rect(ox+3, wing_y, 6, 6, *C_BLACK)
        c.fill_rect(ox+4, wing_y+1, 4, 4, *C_GOLD_L)

    for i in range(4):
        draw_dragon(i, 1, flap=(i % 2) * 3)

    draw_dragon(4, 1, flap=0, is_hurt=True)
    # White flash
    ox = 5 * 32
    c.fill_rect(ox+6, 32+5, 20, 20, *C_WHITE)
    # Crumble
    ox = 6 * 32
    c.fill_rect(ox+8, 32+16, 16, 10, *C_SUIT_DRK)
    ox = 7 * 32
    c.fill_rect(ox+10, 32+22, 12, 6, *C_BLACK)

    c.save(os.path.join(SPRITES_DIR, "enemy.png"))
    print("Dan enemies.png generated.")

# ----------------- 3. VILLAGE TILESET (128 x 128) -----------------
def generate_dan_tileset():
    c = Canvas(128, 128)

    # Tile (0,0): Vibrant Top Grass with Rounded Scallops (16x16)
    # Grass top
    c.fill_rect(0, 0, 16, 6, *C_GRASS_TOP)
    c.fill_rect(0, 1, 16, 4, *C_GRASS_MID)
    # Rounded grass scallops hanging down (3 rounded tufts)
    for tuft in range(4):
        tx = tuft * 4
        c.fill_rect(tx, 6, 4, 2, *C_GRASS_TOP)
        c.fill_rect(tx+1, 7, 2, 2, *C_GRASS_MID)
        c.fill_rect(tx+1, 8, 2, 1, *C_GRASS_DRK)

    # Dirt under grass
    for y in range(9, 16):
        for x in range(16):
            # Chunky brown cobblestone texture
            is_edge = (x % 5 == 0) or (y % 4 == 0)
            c.set_pixel(x, y, *(C_DIRT_DARK if is_edge else C_DIRT_M))
            if (x+y) % 7 == 0:
                c.set_pixel(x, y, *C_DIRT_L)

    # Tile (1,0): Pure Cobblestone / Packed Dirt Wall (16x16)
    ox = 16
    for y in range(16):
        for x in range(16):
            is_edge = (x % 5 == 0) or (y % 4 == 0)
            c.set_pixel(ox+x, y, *(C_DIRT_DARK if is_edge else C_DIRT_M))
            if (x * 3 + y * 7) % 9 < 2:
                c.set_pixel(ox+x, y, *C_DIRT_L)
            elif (x * 5 + y * 3) % 11 < 2:
                c.set_pixel(ox+x, y, *C_DIRT_D)

    # Tile (2,0): Wooden Farm Fence (16x16)
    ox = 32
    # Fence post
    c.fill_rect(ox+2, 2, 3, 14, *C_BLACK)
    c.fill_rect(ox+2, 3, 2, 12, *C_WOOD_L)
    # Two horizontal rails
    c.fill_rect(ox, 4, 16, 3, *C_BLACK)
    c.fill_rect(ox, 5, 16, 2, *C_WOOD_M)
    c.fill_rect(ox, 10, 16, 3, *C_BLACK)
    c.fill_rect(ox, 11, 16, 2, *C_WOOD_M)

    # Tile (3,0): Wooden Wheel / Cart edge (16x16)
    ox = 48
    c.fill_rect(ox+2, 2, 12, 12, *C_BLACK)
    c.fill_rect(ox+3, 3, 10, 10, *C_WOOD_M)
    c.fill_rect(ox+5, 5, 6, 6, *C_WOOD_L)
    c.fill_rect(ox+7, 7, 2, 2, *C_BLACK) # wheel hub

    # Tile (0,1): Half-timbered Cottage Wall (White stucco with black timber frame)
    oy = 16
    c.fill_rect(0, oy, 16, 16, *C_WHITE)
    # Black framing timber
    c.fill_rect(0, oy, 16, 2, *C_BLACK)
    c.fill_rect(0, oy+14, 16, 2, *C_BLACK)
    c.fill_rect(0, oy, 2, 16, *C_BLACK)
    c.fill_rect(14, oy, 2, 16, *C_BLACK)
    # Diagonal timber strut
    for d in range(14):
        c.set_pixel(1+d, oy+1+d, *C_BLACK)
        c.set_pixel(1+d, oy+2+d, 40, 40, 45)

    # Tile (1,1): Cottage Dark Slate Roof (16x16)
    ox = 16
    oy = 16
    c.fill_rect(ox, oy, 16, 16, *C_ROOF_M)
    # Shingle overlapping lines
    for sy in range(0, 16, 4):
        c.fill_rect(ox, oy+sy, 16, 1, *C_ROOF_D)
        c.fill_rect(ox, oy+sy+1, 16, 1, *C_ROOF_L)
        for sx in range((sy % 8), 16, 8):
            c.fill_rect(ox+sx, oy+sy, 1, 4, *C_ROOF_D)

    # Tile (2,1): Arched Wooden Door with Iron Straps (16x16)
    ox = 32
    oy = 16
    c.fill_rect(ox+2, oy+1, 12, 15, *C_BLACK)
    c.fill_rect(ox+3, oy+2, 10, 14, *C_WOOD_M)
    # Iron hinges
    c.fill_rect(ox+3, oy+4, 8, 2, 50, 50, 55)
    c.fill_rect(ox+3, oy+11, 8, 2, 50, 50, 55)
    # Gold handle
    c.fill_rect(ox+10, oy+8, 2, 2, *C_GOLD_L)

    # Tile (3,1): Window with Flower Box (16x16)
    ox = 48
    oy = 16
    c.fill_rect(ox+2, oy+2, 12, 10, *C_BLACK)
    c.fill_rect(ox+3, oy+3, 10, 8, 170, 215, 240) # glass panes
    c.fill_rect(ox+7, oy+3, 2, 8, *C_BLACK) # frame
    c.fill_rect(ox+3, oy+6, 10, 2, *C_BLACK)
    # Flower box with red and yellow blossoms
    c.fill_rect(ox+1, oy+10, 14, 5, *C_WOOD_D)
    c.fill_rect(ox+2, oy+11, 12, 3, *C_WOOD_M)
    c.fill_rect(ox+3, oy+9, 3, 3, *C_SUIT_RED)
    c.fill_rect(ox+7, oy+9, 3, 3, *C_GOLD_L)
    c.fill_rect(ox+11, oy+9, 3, 3, *C_SUIT_RED)

    # Tile (0,2): Golden Haystack / Straw Bale (16x16)
    oy = 32
    c.fill_rect(0, oy+4, 16, 12, *C_BLACK)
    c.fill_rect(1, oy+5, 14, 10, *C_WHEAT_M)
    c.fill_rect(3, oy+3, 10, 12, *C_WHEAT_L)
    # Pitchfork sticking out
    c.fill_rect(10, oy+1, 2, 12, *C_BLACK)
    c.fill_rect(10, oy+2, 1, 10, 190, 190, 200) # steel
    c.fill_rect(8, oy+1, 5, 2, 190, 190, 200)

    # Tile (1,2): Hazard Spikes (Farm caltrops/pitchforks)
    ox = 16
    oy = 32
    for s in range(3):
        sx = ox + 2 + s * 5
        for h in range(8):
            w = 1 + h // 2
            c.fill_rect(sx - w // 2, oy + 14 - h, w, 1, 200, 200, 210)
        c.set_pixel(sx, oy + 14 - 7, *C_SUIT_RED)
    c.fill_rect(ox, oy + 14, 16, 2, *C_BLACK)

    # Tile (2,2): Wooden Storage Crate (16x16)
    ox = 32
    oy = 32
    c.fill_rect(ox+1, oy+1, 14, 14, *C_BLACK)
    c.fill_rect(ox+2, oy+2, 12, 12, *C_WOOD_M)
    # X cross brace
    for b in range(12):
        c.set_pixel(ox+2+b, oy+2+b, *C_WOOD_D)
        c.set_pixel(ox+13-b, oy+2+b, *C_WOOD_D)

    # Tile (3,2): Goal Gate / Exit Shrine
    ox = 48
    oy = 32
    c.fill_rect(ox+2, oy+1, 12, 14, *C_BLACK)
    c.fill_rect(ox+3, oy+2, 10, 12, *C_GOLD_M)
    c.fill_rect(ox+5, oy+4, 6, 8, *C_WHITE) # bright exit portal

    c.save(os.path.join(SPRITES_DIR, "tileset.png"))
    print("Dan tileset.png generated.")

# ----------------- 4. DAYLIGHT VILLAGE BACKGROUND (384 x 216) -----------------
def generate_dan_background():
    c = Canvas(384, 216)

    # 1. Daylight Sky Gradient (Vibrant blue to soft azure)
    for y in range(216):
        t = y / 216.0
        r = int(C_SKY_TOP[0] * (1 - t) + C_SKY_BOT[0] * t)
        g = int(C_SKY_TOP[1] * (1 - t) + C_SKY_BOT[1] * t)
        b = int(C_SKY_TOP[2] * (1 - t) + C_SKY_BOT[2] * t)
        for x in range(384):
            c.set_pixel(x, y, r, g, b)

    # Fluffy white cartoon clouds
    clouds = [(40, 25, 28), (140, 35, 34), (260, 20, 30), (350, 40, 24)]
    for cx, cy, cr in clouds:
        for y in range(cy - cr // 2, cy + cr // 2):
            for x in range(cx - cr, cx + cr):
                d = ((x - cx) / float(cr))**2 + ((y - cy) / float(cr // 2))**2
                if d <= 1.0:
                    c.set_pixel(x, y, *C_WHITE)
                elif d <= 1.15:
                    c.set_pixel(x, y, 220, 240, 255, 180)

    # 2. Distant Light Blue Misty Mountains (y > 70)
    for x in range(384):
        h = int(85 + 28 * math.sin(x * 0.015) + 14 * math.cos(x * 0.035))
        for y in range(max(0, h), 216):
            c.set_pixel(x, y, *C_MNT_FAR)

    # 3. Midground Mountain Ridge with Pine Trees (y > 115)
    for x in range(384):
        h = int(122 + 16 * math.sin(x * 0.03) + 8 * math.sin(x * 0.08))
        # Pine tree jagged peaks
        if (x % 9) == 0:
            h -= 8
        elif (x % 9) == 1 or (x % 9) == 8:
            h -= 5
        for y in range(max(0, h), 216):
            c.set_pixel(x, y, *C_PINES)

    # 4. Rolling Golden Wheat Fields & Farm Fences (y > 152)
    for x in range(384):
        h = int(158 + 10 * math.sin(x * 0.02) + 4 * math.cos(x * 0.05))
        for y in range(max(0, h), 216):
            # Alternating golden wheat stripes
            is_stripe = ((x + y // 2) % 12) < 4
            c.set_pixel(x, y, *(C_WHEAT_L if is_stripe else C_WHEAT_M))

    # Little wooden farm fences in midground
    for fx in range(30, 380, 45):
        fy = int(158 + 10 * math.sin(fx * 0.02) + 4 * math.cos(fx * 0.05)) - 8
        c.fill_rect(fx, fy, 2, 8, *C_WOOD_M)
        c.fill_rect(fx - 15, fy + 2, 30, 2, *C_WOOD_M)

    c.save(os.path.join(SPRITES_DIR, "parallax_bg.png"))
    print("Dan parallax_bg.png generated.")

# ----------------- 5. UPBEAT DAN THE MAN RETRO ARCADE BGM & SFX -----------------
def generate_dan_audio():
    sample_rate = 22050
    rng = random.Random(77)

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

    # 1. PUNCH IMPACT (Crunchy smack!)
    punch_samples = []
    dur = 0.12
    n = int(sample_rate * dur)
    for i in range(n):
        t = i / float(sample_rate)
        env = math.exp(-t * 35.0)
        thud = math.sin(2.0 * math.pi * 140.0 * t) * 16000.0
        noise = rng.uniform(-1.0, 1.0) * 18000.0 if t < 0.04 else 0.0
        punch_samples.append((thud + noise) * env)
    write_wav(os.path.join(AUDIO_DIR, "hit.wav"), punch_samples)

    # 2. MARTIAL ARTS SWOOSH
    slash_samples = []
    dur = 0.10
    n = int(sample_rate * dur)
    for i in range(n):
        t = i / float(sample_rate)
        env = math.sin(t / dur * math.pi)
        freq = 3200.0 * (1.0 - t/dur) + 400.0
        noise = rng.uniform(-1.0, 1.0)
        val = noise * math.sin(2.0 * math.pi * freq * t) * 18000.0 * env
        slash_samples.append(val)
    write_wav(os.path.join(AUDIO_DIR, "slash.wav"), slash_samples)

    # 3. COIN PICKUP (Cheerful arcade ding!)
    coin_samples = []
    notes = [987.77, 1318.51] # B5 -> E6
    dur_sub = 0.05
    for f in notes:
        n_sub = int(sample_rate * dur_sub)
        for i in range(n_sub):
            t = i / float(sample_rate)
            env = 1.0 - (t / dur_sub) * 0.3
            phase = (t * f) % 1.0
            sq = 14000 if phase < 0.5 else -14000
            coin_samples.append(sq * env)
    write_wav(os.path.join(AUDIO_DIR, "pickup.wav"), coin_samples)

    # 4. COMIC JUMP (Boing / Spring chirp)
    jump_samples = []
    dur = 0.13
    n = int(sample_rate * dur)
    for i in range(n):
        t = i / float(sample_rate)
        freq = 280.0 + 600.0 * (t / dur) ** 0.7
        phase = (t * freq) % 1.0
        sq = 13000 if phase < 0.5 else -13000
        env = 1.0 - (t / dur)
        jump_samples.append(sq * env)
    write_wav(os.path.join(AUDIO_DIR, "jump.wav"), jump_samples)

    # 5. FOOTSTEP
    step_samples = []
    dur = 0.035
    n = int(sample_rate * dur)
    for i in range(n):
        t = i / float(sample_rate)
        env = 1.0 - (t / dur)
        step = (math.sin(2.0 * math.pi * 120.0 * t) * 7000.0 + rng.uniform(-1.0, 1.0) * 3500.0) * env
        step_samples.append(step)
    write_wav(os.path.join(AUDIO_DIR, "footstep.wav"), step_samples)

    # 6. ENEMY POP / JETPACK DEFEAT
    pop_samples = []
    dur = 0.22
    n = int(sample_rate * dur)
    for i in range(n):
        t = i / float(sample_rate)
        env = 1.0 - (t / dur)
        freq = 380.0 * (1.0 - t/dur) + 80.0
        sq = 11000 if ((t * freq) % 1.0) < 0.5 else -11000
        noise = rng.uniform(-1.0, 1.0) * 8000.0
        pop_samples.append((sq + noise) * env)
    write_wav(os.path.join(AUDIO_DIR, "enemy_die.wav"), pop_samples)

    # 7. UPBEAT ACTION ARCADE BGM (140 BPM, Happy/Heroic Action)
    # Key: C Major / A Minor: C -> G -> Am -> F (Infectious heroic arcade groove!)
    print("Synthesizing high-energy Dan-style arcade BGM...")
    bpm = 140.0
    beat_dur = 60.0 / bpm
    total_beats = 16 # 4 bars of 4/4
    total_dur = total_beats * beat_dur
    n_bgm = int(sample_rate * total_dur)
    bgm_samples = [0.0] * n_bgm

    chords = [
        {"root": 65.41,  "lead": [523.25, 587.33, 659.25, 783.99]}, # C (C5, D5, E5, G5)
        {"root": 49.00,  "lead": [392.00, 493.88, 587.33, 783.99]}, # G (G4, B4, D5, G5)
        {"root": 55.00,  "lead": [440.00, 523.25, 659.25, 880.00]}, # Am (A4, C5, E5, A5)
        {"root": 43.65,  "lead": [349.23, 440.00, 523.25, 698.46]}, # F (F4, A4, C5, F5)
    ]

    for beat in range(total_beats):
        bar = beat // 4
        chord = chords[bar]
        start_t = beat * beat_dur
        start_idx = int(start_t * sample_rate)

        # 1. Bouncy Slap Bass (Octave bouncing!)
        bass_f = chord["root"]
        bass_n = int(beat_dur * 0.9 * sample_rate)
        for i in range(bass_n):
            if start_idx + i < n_bgm:
                t = i / float(sample_rate)
                # Octave jump on upbeat
                f_cur = bass_f * 2.0 if (t > beat_dur * 0.5) else bass_f
                env = math.exp(-((t % (beat_dur * 0.5)) * 6.0))
                # Saw / square hybrid
                sq = 6500 if ((t * f_cur) % 1.0) < 0.5 else -6500
                bgm_samples[start_idx + i] += sq * env

        # 2. Punchy 4-on-the-floor Kick + Snare
        is_snare = (beat % 2 == 1)
        drum_n = int(0.09 * sample_rate)
        for i in range(drum_n):
            if start_idx + i < n_bgm:
                t = i / float(sample_rate)
                env = 1.0 - t / 0.09
                if is_snare:
                    snare_noise = rng.uniform(-1.0, 1.0) * 5500.0 * env
                    bgm_samples[start_idx + i] += snare_noise
                else:
                    k_f = 140.0 * (1.0 - t/0.09) + 45.0
                    kick = math.sin(2.0 * math.pi * k_f * t) * 7500.0 * env
                    bgm_samples[start_idx + i] += kick

        # 3. Upbeat Arcade Lead Melody & Arp (Catchy, cheerful!)
        sub_n = int(beat_dur / 4.0 * sample_rate)
        for sub in range(4):
            sub_idx = start_idx + sub * sub_n
            # Play upbeat melodic line
            note_idx = (beat * 2 + sub) % 4
            melody_f = chord["lead"][note_idx]
            for i in range(int(sub_n * 0.85)):
                if sub_idx + i < n_bgm:
                    t = i / float(sample_rate)
                    env = 1.0 - (i / float(sub_n * 0.85)) * 0.3
                    phase = (t * melody_f) % 1.0
                    sq = 3800 if phase < 0.35 else -3800
                    bgm_samples[sub_idx + i] += sq * env

    write_wav(os.path.join(AUDIO_DIR, "bgm.wav"), bgm_samples)
    print("Dan arcade bgm.wav generated.")

if __name__ == "__main__":
    generate_dan_player()
    generate_dan_enemies()
    generate_dan_tileset()
    generate_dan_background()
    generate_dan_audio()
    print("All Dan-style pixel art assets and arcade audio successfully built!")
