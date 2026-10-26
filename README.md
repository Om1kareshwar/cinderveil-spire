# Dan's Village Brawler (Retro Pixel Art Action Platformer)

A retro arcade action platformer and beat-'em-up prototype built in **Godot 4.3 (GDScript)** inspired directly by the vibrant, comedic art style of **Halfbrick's *Dan the Man***. Features comic pixel art characters, high-energy retro arcade chiptune music, punch-and-baton combat, speech bubble reactions, and medieval farm village scenery.

---

## 🎵 Dramatic Soundtrack & Dynamic Audio Engine

1. **Dramatic Default Soundtrack (`assets/audio/bgm.wav`):**
   * A driving, cinematic 136 BPM action soundtrack in D Minor (Dm -> B♭ -> Gm -> A7).
   * Pounding battle timpani, military snares, intense 16th-note driving bass, minor string stabs, and an urgent heroic lead melody that keeps you on the edge of your seat.
2. **Dramatic "Lost a Heart" Audio SFX (`assets/audio/heart_lost.wav`):**
   * Triggers dynamically every time Dan loses a heart (takes damage or falls off a ledge).
   * Features a jarring 4-note descending minor dissonance cascade (`F5 -> D5 -> A♭4 -> D4`), a heavy sub-bass drop (`220 Hz -> 45 Hz`), and a glass/heart fracture transient crunch.
3. **Dramatic Game Over Soundtrack (`assets/audio/game_over.wav`):**
   * Automatically cuts off the main BGM and plays a somber, cinematic ~7.5-second funeral defeat march (72 BPM) when all 5 hearts are depleted.
   * Features slow echoing timpani booms, somber minor chord pads, and a mournful descending chiptune music box melody (`D5 -> C#5 -> B♭4 -> A4 -> F4 -> E4 -> D4 -> D3 bell toll`).
   * Seamlessly restarts the dramatic default soundtrack when pressing **`[R]`** to try again!

---

## 🎨 Visual Art Style (*Dan the Man Village Aesthetic*)

* **Player Character (Dan-Style Brawler):**
  * Blocky cartoon character with black side-part hair, expressive eyes, sleeveless dark tactical vest with belt buckle, and combat boots.
  * **Comic Speech Bubble `[ ! ]`:** Pops up over Dan's head with a bouncy pop animation on spawn and during encounters.
  * **Attacks:** Alternates between a bare-knuckle power punch (with white comic swoosh) and a wooden baton/club swing (with yellow action smear).
* **Enemies:**
  * **Red Jetpack Ninjas:** Red hooded combat suits, white goggle visors, and twin thrusters emitting bright flames and smoke puffs.
  * **Flying Red Dragon Mascot:** Cartoon dragon head costume with sharp white teeth, yellow horns, and green underbelly.
  * **Village Guard:** Helmeted guard with purple plume.
* **Village & Farm Scenery:**
  * **Daylight Parallax Sky:** Saturated bright blue sky with fluffy cartoon clouds, distant misty blue mountains, dark pine forest ridges, and golden rolling wheat fields with farm fences.
  * **Ground & Platforms:** Neon lime green grass with rounded scalloped tufts hanging over chunky packed brown cobblestone/pebble earth.
  * **Farm Props:** Golden haystack with a steel pitchfork, wooden farm cart with spoked wheels, and stacked wooden storage crates.
  * **Half-Timbered Village Cottage:** Dark slate shingle roof (jumpable platform!), white plastered walls with black timber beams, rustic arched wooden door with iron straps, and a window with a flower planter box.
* **HUD Layout:**
  * **Top-Left:** Dragon avatar badge + glowing green HP bar with smooth tween animations + red potion bottle icon.
  * **Top-Right:** Large smiling Gold Coin icon + 6-digit score/coin counter (`001990` style) inside a dark rounded capsule + `[ || ]` Pause button.

---

## 🕹️ Controls

| Action | Keyboard / Mouse |
| :--- | :--- |
| **Move Left / Right** | <kbd>A</kbd> / <kbd>D</kbd> or <kbd>←</kbd> / <kbd>→</kbd> |
| **Jump** | <kbd>Space</kbd> / <kbd>W</kbd> / <kbd>↑</kbd> *(hold for high jump, tap for short hop)* |
| **Attack (Punch / Baton)**| <kbd>J</kbd> or **Left Mouse Click** *(combos between punch & stick swing)* |
| **Restart / Play Again** | <kbd>R</kbd> *(works anytime, or upon Knockout / Victory)* |

---

## 🚀 Running the Game

### Quick Launch (Windows)
Double-click **`Run_Game.bat`** in this directory to launch the game window immediately!

### In Godot 4.3 Editor
Double-click **`Open_In_Godot_Editor.bat`** or import `project.godot` inside Godot 4.3.
