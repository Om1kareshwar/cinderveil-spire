# Cinderveil: Embers of the Spire

A complete 2D Dark Fantasy Action-Platformer / Hack-and-Slash prototype built from scratch in **Godot 4.3 (GDScript)** featuring 16-bit retro pixel art, responsive kinematic movement with coyote time and jump buffering, melee combat, patrolling enemy AI, and procedural chiptune audio.

---

## 🎮 Features

* **Kinematic Platforming Physics:**
  * Mathematically calculated jump arcs via `jump_height` and `time_to_peak`.
  * **Coyote Time (120ms):** Allows jumping just after leaving a platform edge.
  * **Jump Buffering (140ms):** Queues jump input before touching the ground.
  * **Variable Jump Height:** Releasing the jump button early cuts upward momentum for precision aerial control.
* **Combat & Game Feel:**
  * Forward lunging melee sword slash with active hitbox synchronization.
  * Invulnerability frames (i-frames) and visual white damage flash.
  * Screen shake trauma and impact feedback.
* **Intelligent Enemy AI:**
  * Patrolling skeleton warriors that detect platform edges and walls using RayCasts.
  * Dynamic player detection and chasing logic.
  * Health component, knockback physics, and loot dropping on defeat.
* **Level & Hazards:**
  * Floating platforms, pit spikes, collectibles (Cinder Embers), and an ancient exit portal shrine.
  * Multi-layer Parallax background with gothic spires, moonlit sky, and stars.
* **Full Chiptune Audio Engine:**
  * Procedurally synthesized 8-bit / 16-bit sound effects (jump, sword swing, hit crunch, coin pickup, footsteps, enemy death).
  * Looping 16-bar retro chiptune background music (Dm -> Bb -> C -> Am chord progression).

---

## 🕹️ Controls

| Action | Keyboard / Mouse |
| :--- | :--- |
| **Move Left / Right** | `A` / `D` or `Left Arrow` / `Right Arrow` |
| **Jump** | `Space` or `W` or `Up Arrow` |
| **Attack (Melee Slash)** | `J` or `Left Mouse Button` |
| **Restart Level** | `R` (available anytime or after Death / Victory) |

---

## 🎨 Art & Color Palette (*"Ash & Amethyst"*)

The game uses a curated 16-color dark fantasy palette designed for crisp integer pixel scaling:
* **Void Abyss:** `#0d0f1b`
* **Obsidian Slate:** `#181b2c`
* **Twilight Indigo:** `#2a2d4a`
* **Crypt Stone:** `#43486b`
* **Weathered Basalt:** `#686f99`
* **Ash Grey:** `#9da4c4`
* **Silver Fog:** `#e0e6f8`
* **Cinder Maroon:** `#451624`
* **Fiery Crimson:** `#841e33`
* **Molten Ember:** `#c93b2b`
* **Sunfire Orange:** `#e86a23`
* **Radiance Gold:** `#f4b436`
* **Solar Yellow:** `#ffe869`
* **Spectral Cyan:** `#52d6b6`

---

## 🚀 Running the Game

### Quick Launch (Windows)
Double-click `Run_Game.bat` inside this repository to launch the game immediately in Godot 4.3!

### In Godot Editor
1. Open **Godot 4.3**.
2. Click **Import** and select the `project.godot` file in this directory.
3. Press **F5** (or the Play button in the top right) to run the project.

---

## 📁 Repository Structure

```
cinderveil-spire/
├── project.godot               # Engine configuration & viewport settings
├── Run_Game.bat                # 1-click game launcher
├── Open_In_Godot_Editor.bat    # 1-click editor launcher
├── assets/
│   ├── sprites/                # 2D pixel art character, enemy, tileset & parallax bg
│   └── audio/                  # Retro sound effects & looping chiptune BGM
├── scripts/
│   ├── game_manager.gd         # Singleton managing HP, Embers, and signals
│   ├── sound_manager.gd        # Singleton managing SFX and looping music
│   ├── player.gd               # Responsive CharacterBody2D controller
│   ├── enemy_skeleton.gd       # Edge/wall detecting patrol & chase AI
│   ├── ember_pickup.gd         # Animated floating collectible
│   ├── spikes_hazard.gd        # Spike hazard script
│   ├── exit_shrine.gd          # Level completion trigger
│   ├── camera_controller.gd    # Smooth camera with trauma shake
│   └── hud.gd                  # Heart HUD, Ember counter & Game Over screens
└── scenes/
    ├── player.tscn             # Player CharacterBody2D scene
    ├── enemy_skeleton.tscn     # Skeleton Grunt enemy scene
    ├── ember_pickup.tscn       # Collectible scene
    ├── spikes.tscn             # Hazard scene
    ├── exit_shrine.tscn        # Level goal scene
    ├── hud.tscn                # CanvasLayer UI scene
    └── main.tscn               # Root playable game world
```
