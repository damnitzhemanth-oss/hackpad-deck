# MacroPad
A 9-key *multi-functional* macropad with rotary encoder, OLED, and addressable RGB LEDs

*Note : This ReadMe is written by a human known as Hemanth from India, I am new to this and learning every day. Please highlight the mistakes I may have made.*

## Overview

This is my first **Stardance HackClub** project. I have officially worked on this project for 22+ hours. I want to thank all the people to who are responsible in creation of these organizations. 

## Functions 

- Modes like Dev, Editor, etc with different presets of keys.
- Contains a satisfying Mini Game.
(*Discussed in **depth** in upcoming sections*)

![Assembly Render](<CAD/renders/Assembly Main View.png>)

## PCB  Design

I was already well versed with simple hardware projects using **Arduino UNO** and **ESP 8266**, but even though I knew about PCBs I never used them as they are expensive. Learning *KiCad* was pretty straight forward and easy.

Mainly routing was a bit challenging but everything else was easy. DRC have 0 errors except silkscreen warnings. 

## PCB Gallery

1. SCHEMATIC SVG 

![Schematic Picture](<PCB/renders/MACROPAD.svg>)

2. Screenshots

![Schematic Picture](<PCB/renders/Microcontroller_Hackpad.png>)
![Schematic Picture](<PCB/renders/Encoder+OLED_Hackpad.png>)
![Schematic Picture](<PCB/renders/LED_Matrix_Hackpad.png>)
![Schematic Picture](<PCB/renders/Switch_matrix_hackpad.png>)
![Schematic Picture](<PCB/renders/PCB.png>)
![Schematic Picture](<PCB/renders/PCB_3d.png>)

## CAD Design

Cad was one of the field I had zero ball knowledge about. So designing it was fun but also was a pain. Due to daily internet cap I was not able to download Fusion 360, so OnShape was the way to go.
The design mainly consists of Base plate with Heatset Inserts and Top Plate with holes for M3 screws. PCB gets sandwiched between. All this was done in keeping +0.2 mm tolerance in mind.

## Cad Gallery.

![Assembly Render](<CAD/renders/Assembly Main View.png>)
![Assembly Render](<CAD/renders/Back View.png>)
![Assembly Render](<CAD/renders/Front View.png>)
![Plates](<CAD/renders/Top_Plate .png>)
![Plates](<CAD/renders/Top_Plate2.png>)
![Plates](<CAD/renders/Base_Plate.png>)
![Plates](<CAD/renders/Base_Plate2.png>)

##  Functions

| Feature | Description |
|---------|-------------|
|  **6 Modes** | Dev, Media, Video, Macro, Aesthetic, Games |
|  **Whack-a-LED Game** | Press the lit switch before time runs out |
| **DJ Mode** | Rainbow RGB animation across all 9 LEDs |
|  **Snowfall OLED** | Idle screen shows falling snowflakes |
|  **Rotary Encoder** | Volume control on every mode |
| **Per-Key RGB** | 9 addressable SK6812MINI-E LEDs |
|  **Live OLED Feedback** | Shows mode, key presses, and game score |

---

##  Modes

Cycle modes by **long-pressing SW7** (bottom-left key).

### 1. DEV — Editor & Typing
| Key | Action |
|-----|--------|
| SW1–SW9 | Number keys 2–9 (numpad layout) |
| SW7 (tap) | ESC |
| SW7 (hold) | Next mode |

### 2. MEDIA — Playback Controls
| Key | Action |
|-----|--------|
| SW1 | Play / Pause |
| SW2 | Stop |
| SW3 | Mute |
| SW4 | Previous Track |
| SW6 | Next Track |
| SW8 | Volume Down |
| SW9 | Volume Up |

### 3. VIDEO — DaVinci Resolve Editing
| Key | Action |
|-----|--------|
| SW1 | Split Clip |
| SW2 | Undo |
| SW3 | Redo |
| SW4 | Mark In |
| SW5 | Mark Out |
| SW6 | Paste Attributes |
| SW8 | Play / Pause |
| SW9 | Backspace |

### 4. MACRO — Launcher & Productivity
| Key | Action |
|-----|--------|
| SW1–SW3 | Open App 1 / 2 / 3 |
| SW4–SW6 | Copy / Paste / Cut |
| SW8–SW9 | Select All / Save |

### 5. AESTHETIC — DJ Mode 
RGB LEDs dance through a rotating rainbow. No key output — pure visual vibes.

### 6. GAMES — Whack-a-LED 
A random LED lights up **green**. Press its switch within **3 seconds** to score. Wrong key or timeout resets your score to 0 and flashes all LEDs red.

---


## Bill of Materials

| # | Component | Qty | Source |
|---|-----------|-----|--------|
| 1 | Seeed XIAO RP2040 | 1 | Hack Club Kit |
| 2 | Gateron KS-3 MX Switches | 9 | Hack Club Kit |
| 3 | 1N4148 Through-hole Diodes | 9 | Hack Club Kit |
| 4 | Alps EC11E Rotary Encoder | 1 | Hack Club Kit |
| 5 | SK6812MINI-E RGB LEDs | 9 | Hack Club Kit |
| 6 | 0.91" SSD1306 OLED Display (128×32) | 1 | Hack Club Kit |
| 7 | White DSA Keycaps | 9 | Hack Club Kit |
| 8 | M3×16mm Screws *(trim to 13mm)* | 4 | Hack Club Kit |
| 9 | M3×5mm×4mm Heatset Inserts | 4 | Hack Club Kit |
| 10 | 3D Printed Case (Base + Top Plate) | 1 set | 


---

## Firmware

Written in **Python** using **KMK** on **CircuitPython**.

See [`Firmware/main.py`](Firmware/main.py) for the full source.

---

## AI USAGE

I used AI/ Online resources to learn but never automate anything. You can checkout Lapse recording from lookout too.

## Credits

- **[Hack Club](https://hackclub.com/)** — for the kit and the program
- **Star Dance** — for organizing this buildathon
- **[KMK Firmware](https://github.com/KMKfw/kmk_firmware)** — Python keyboard firmware
- **Hack Club Hackpad team** — for the guides and KiCad care package
- Special shoutout to Logan Peterson, whose design inspired me a lot.

---

##  License

Open source, but you are responsible if it creates a black hole in your house.


