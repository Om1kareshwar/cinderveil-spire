# Dan's Village Brawler (Retro Pixel Art Action Platformer)

A retro arcade action platformer and beat-'em-up prototype built in **Godot 4.3 (GDScript)** inspired directly by the vibrant, comedic art style of **Halfbrick's *Dan the Man***. Features comic pixel art characters, high-energy retro arcade chiptune music, punch-and-baton combat, speech bubble reactions, and medieval farm village scenery.

---

## 🎨 Visual Art Style (*Dan the Man Village Aesthetic*)

* **Player Character (Dan-Style Brawler):**
  * Blocky head with classic short dark hair and expressive cartoon eyes.
  * Black sleeveless tactical vest with belt buckle, dark grey combat trousers, and boots.
  * **Comic Speech Bubble `[ ! ]`:** Bounces over Dan's head when starting the level or encountering enemies!
  * **Combat Animations:** Snappy bare-knuckle power punch with white action whoosh and wooden baton club swing with yellow action smears.
* **Enemies:**
  * **Red Jetpack Ninjas:** Red hooded combat suits, white visors/goggles, dual thrusters emitting flame exhaust and smoke puffs!
  * **Flying Red Dragon Mascot:** Giant cartoon dragon head costume with sharp white teeth, yellow horns, and green underbelly.
  * **Village Guards:** Medieval helmet with purple plume, patrolling roofs and platforms.
* **Environment & Village Scenery:**
  * **Parallax Backdrop:** Bright sunny blue sky with fluffy cartoon clouds, distant misty blue mountains, dark pine forest ridges, and golden rolling wheat fields with farm fences.
  * **Ground & Platforms:** Vibrant neon green grass with rounded scalloped grass tufts hanging over chunky packed brown cobblestone earth.
  * **Village Props:** Golden haystacks with pitchforks, wooden farm cart with spoked wheels, stacked wooden shipping crates, and a medieval half-timbered cottage with dark slate roof shingles, white stucco walls, black timber beams, arched wooden door, and flower box window!
* **HUD Layout (Direct Screenshot Match):**
  * **Top-Left:** Dragon avatar badge + glowing green HP bar with smooth tweening + red potion bottle counter.
  * **Top-Right:** Large smiling gold coin icon + 6-digit score/coin counter (`001990` style) inside a dark rounded capsule box + Pause button `[ || ]`.

---

## 🎵 High-Energy Retro Arcade BGM & SFX

* **Background Music (`bgm.wav`):**
  * High-energy, infectious 140 BPM arcade action chiptune in C Major / A Minor (C -> G -> Am -> F).
  * Driving 4-on-the-floor kick and snappy snare.
  * Bouncy slap bass jumping octaves on the upbeat.
  * Heroic, cheerful retro lead melody and fast arpeggios inspired by classic arcade brawlers!
* **Sound Effects (SFX):**
  * `hit.wav`: Crunchy cartoon impact smack.
  * `slash.wav`: Crisp martial arts swoosh.
  * `pickup.wav`: Cheerful two-tone arcade coin ding (`987 Hz` -> `1318 Hz`).
  * `jump.wav`: Comic spring boing / chirp.
  * `footstep.wav`: Light running thud.
  * `enemy_die.wav`: Comedic jetpack pop / defeat crunch.

---

## 🕹️ Controls

| Action | Keyboard / Mouse |
| :--- | :--- |
| **Move Left / Right** | <kbd>A</kbd> / <kbd>D</kbd> or <kbd>←</kbd> / <kbd>→</kbd> |
| **Jump** | <kbd>Space</kbd> or <kbd>W</kbd> or <kbd>↑</kbd> *(hold for high jump, tap for short hop)* |
| **Attack (Punch / Baton)**| <kbd>J</kbd> or **Left Mouse Click** *(combos between punch & stick swing)* |
| **Restart / Play Again** | <kbd>R</kbd> *(works anytime, or upon Knockout / Victory)* |

---

## 🚀 Running the Game

### Quick Launch (Windows)
Double-click **`Run_Game.bat`** in this directory to launch the game window immediately!

### In Godot 4.3 Editor
Double-click **`Open_In_Godot_Editor.bat`** or import `project.godot` inside Godot 4.3.
