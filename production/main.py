import board
import time
import random
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, Key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.holdtap import HoldTap
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.modules import Module

keyboard = KMKKeyboard()

keyboard.row_pins = (board.D0, board.D1, board.D2)
keyboard.col_pins = (board.D3, board.D6, board.D7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

MODE_NAMES = ["DEV", "MEDIA", "VIDEO", "MACRO", "AESTHETIC", "GAMES"]
current_mode = 0

MODE_COLORS = {
    0: {"idle": (0, 0, 40),    "accent": (255, 255, 255)},
    1: {"idle": (40, 0, 40),   "accent": (0, 255, 60)},
    2: {"idle": (50, 20, 0),   "accent": (0, 200, 255)},
    3: {"idle": (40, 0, 0),    "accent": (255, 220, 0)},
    4: {"idle": (0, 0, 0),     "accent": (0, 0, 0)},
    5: {"idle": (0, 0, 0),     "accent": (0, 0, 0)},
}

keyboard.active_layers = [current_mode]

layers_ext = Layers()
keyboard.modules.append(layers_ext)


class ModeCycleKey(Key):
    def on_press(self, keyboard):
        global current_mode
        current_mode = (current_mode + 1) % len(MODE_NAMES)
        keyboard.active_layers = [current_mode]
        status.on_mode_changed()


MODE_CYCLE = ModeCycleKey()

hold_tap = HoldTap(tap_time=200)
keyboard.modules.append(hold_tap)

SW7_HOLDTAP = KC.HT(KC.ESC, MODE_CYCLE)

keyboard.keymap = [
    [
        KC.N7, KC.N8, KC.N9,
        KC.N4, KC.N5, KC.N6,
        SW7_HOLDTAP, KC.N2, KC.N3,
    ],
    [
        KC.MPLY, KC.MSTP, KC.MUTE,
        KC.MPRV, KC.NO,   KC.MNXT,
        SW7_HOLDTAP, KC.VOLD, KC.VOLU,
    ],
    [
        KC.LCTL(KC.LSFT(KC.N3)),
        KC.LCTL(KC.Z),
        KC.LCTL(KC.LSFT(KC.Z)),
        KC.I,
        KC.O,
        KC.LCTL(KC.LSFT(KC.V)),
        SW7_HOLDTAP, KC.SPC, KC.BSPC,
    ],
    [
        KC.LGUI(KC.N1), KC.LGUI(KC.N2), KC.LGUI(KC.N3),
        KC.LCTL(KC.C),  KC.LCTL(KC.V),  KC.LCTL(KC.X),
        SW7_HOLDTAP,    KC.LCTL(KC.A),  KC.LCTL(KC.S),
    ],
    [
        KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO,
        SW7_HOLDTAP, KC.NO, KC.NO,
    ],
    [
        KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO,
        SW7_HOLDTAP, KC.NO, KC.NO,
    ],
]

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = ((board.D9, board.D10, None),)
encoder_handler.map = [((KC.VOLD, KC.VOLU),)]

rgb_ext = RGB(
    pixel_pin=board.D8,
    num_pixels=9,
    animation_mode=AnimationModes.STATIC,
    val_limit=100,
)
keyboard.extensions.append(rgb_ext)

LED_CHAIN_ORDER = [1, 2, 3, 9, 8, 7, 6, 5, 4]
SW_TO_LED_INDEX = {sw: idx for idx, sw in enumerate(LED_CHAIN_ORDER)}
LED_INDEX_TO_SW = {idx: sw for sw, idx in SW_TO_LED_INDEX.items()}

COORD_TO_SW = {
    (0, 0): 1, (0, 1): 2, (0, 2): 3,
    (1, 0): 4, (1, 1): 5, (1, 2): 6,
    (2, 0): 7, (2, 1): 8, (2, 2): 9,
}


def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c
    if   h < 60:  r, g, b = c, x, 0
    elif h < 120: r, g, b = x, c, 0
    elif h < 180: r, g, b = 0, c, x
    elif h < 240: r, g, b = 0, x, c
    elif h < 300: r, g, b = x, 0, c
    else:         r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))


displayio.release_displays()
i2c = busio.I2C(board.D5, board.D4)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

text_group = displayio.Group()
mode_label = label.Label(terminalio.FONT, text="DEV", x=4, y=8, scale=2)
key_label  = label.Label(terminalio.FONT, text="", x=4, y=24, scale=1)
text_group.append(mode_label)
text_group.append(key_label)

snow_bitmap = displayio.Bitmap(128, 32, 2)
snow_palette = displayio.Palette(2)
snow_palette[0] = 0x000000
snow_palette[1] = 0xFFFFFF
snow_tile = displayio.TileGrid(snow_bitmap, pixel_shader=snow_palette)
snow_group = displayio.Group()
snow_group.append(snow_tile)

display.root_group = text_group

MAX_SNOW = 35
snow_x = [random.randint(0, 127) for _ in range(MAX_SNOW)]
snow_y = [random.randint(0, 31)  for _ in range(MAX_SNOW)]


def draw_snowfall():
    snow_bitmap.fill(0)
    for i in range(MAX_SNOW):
        if 0 <= snow_x[i] < 128 and 0 <= snow_y[i] < 32:
            snow_bitmap[snow_x[i], snow_y[i]] = 1
        snow_y[i] += 1
        if random.random() > 0.5:
            snow_x[i] += random.randint(-1, 1)
            snow_x[i] = max(0, min(127, snow_x[i]))
        if snow_y[i] >= 32:
            snow_y[i] = 0
            snow_x[i] = random.randint(0, 127)


def show_text_mode(mode_name, key_text=""):
    mode_label.text = mode_name
    key_label.text = key_text
    display.root_group = text_group


def show_snow_mode():
    display.root_group = snow_group


GAME_TIMEOUT = 3.0

game_target    = 1
game_score     = 0
game_lit_at    = 0.0
game_reset_until = 0.0


def game_start_round():
    global game_target, game_lit_at, game_reset_until
    game_target = random.randint(1, 9)
    game_lit_at = time.monotonic()
    game_reset_until = 0
    for i in range(9):
        rgb_ext.pixels[i] = (0, 0, 0)
    rgb_ext.pixels[SW_TO_LED_INDEX[game_target]] = (0, 255, 100)


def game_reset_score():
    global game_score, game_reset_until
    game_score = 0
    game_reset_until = time.monotonic() + 0.5
    for i in range(9):
        rgb_ext.pixels[i] = (255, 0, 0)


IDLE_TIMEOUT   = 3.0
FRAME_INTERVAL = 0.05
FLASH_DURATION = 0.15


class HackPadStatus(Module):

    def __init__(self):
        self.last_activity   = time.monotonic()
        self.last_frame      = 0.0
        self.snowfall_active = False
        self.flash_queue     = []

    def during_bootup(self, keyboard):
        self.apply_idle_rgb()
        show_text_mode(MODE_NAMES[current_mode], "Ready")
        return keyboard

    def before_matrix_scan(self, keyboard):
        now = time.monotonic()
        mode_name = MODE_NAMES[current_mode]

        if self.flash_queue and now >= self.flash_queue[0][1]:
            for pixel_idx, expire in list(self.flash_queue):
                if now >= expire:
                    self.flash_queue.remove((pixel_idx, expire))
                    if mode_name not in ("AESTHETIC", "GAMES"):
                        rgb_ext.pixels[pixel_idx] = MODE_COLORS[current_mode]["idle"]

        if now - self.last_frame >= FRAME_INTERVAL:
            self.last_frame = now

            if mode_name == "AESTHETIC":
                self._animate_aesthetic(now)
            elif mode_name == "GAMES":
                self._animate_games(now)
            elif self.snowfall_active:
                draw_snowfall()

        if mode_name not in ("GAMES",):
            idle_time = now - self.last_activity
            if idle_time > IDLE_TIMEOUT and not self.snowfall_active:
                self.snowfall_active = True
                show_snow_mode()
            elif idle_time <= IDLE_TIMEOUT and self.snowfall_active:
                self.snowfall_active = False
                show_text_mode(MODE_NAMES[current_mode], "Ready")

        return keyboard

    def after_matrix_scan(self, keyboard):
        return keyboard

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if int_coord is None:
            return key

        row = int_coord // len(keyboard.col_pins)
        col = int_coord % len(keyboard.col_pins)
        sw = COORD_TO_SW.get((row, col))
        if sw is None:
            return key

        mode_name = MODE_NAMES[current_mode]

        if mode_name == "GAMES":
            if is_pressed:
                self._handle_game_press(sw)
            return None

        if is_pressed:
            self.last_activity = time.monotonic()
            self.snowfall_active = False
            self._flash_key(sw)
            self._show_text(sw)

        return key

    def before_hid_send(self, keyboard):
        return keyboard

    def after_hid_send(self, keyboard):
        return keyboard

    def on_powersave_enable(self, keyboard):
        return keyboard

    def on_powersave_disable(self, keyboard):
        return keyboard

    def on_mode_changed(self):
        global game_score
        self.last_activity = time.monotonic()
        self.snowfall_active = False

        mode_name = MODE_NAMES[current_mode]

        if mode_name == "GAMES":
            game_score = 0
            game_start_round()
            show_text_mode("GAMES", "Score: 0")
        elif mode_name == "AESTHETIC":
            for i in range(9):
                rgb_ext.pixels[i] = (0, 0, 0)
            show_text_mode("AESTHETIC", "DJ mode")
        else:
            self.apply_idle_rgb()
            show_text_mode(mode_name, "Ready")

    def apply_idle_rgb(self):
        mode_name = MODE_NAMES[current_mode]
        if mode_name in ("AESTHETIC", "GAMES"):
            return
        color = MODE_COLORS[current_mode]["idle"]
        for i in range(9):
            rgb_ext.pixels[i] = color

    def _flash_key(self, sw):
        if MODE_NAMES[current_mode] in ("AESTHETIC", "GAMES"):
            return
        pixel_idx = SW_TO_LED_INDEX.get(sw)
        if pixel_idx is None:
            return
        accent = MODE_COLORS[current_mode]["accent"]
        rgb_ext.pixels[pixel_idx] = accent
        self.flash_queue.append((pixel_idx, time.monotonic() + FLASH_DURATION))

    def _show_text(self, sw):
        show_text_mode(MODE_NAMES[current_mode], "SW{}".format(sw))

    def _animate_aesthetic(self, now):
        phase = (now * 300) % 360
        for i in range(9):
            hue = (phase + i * 40) % 360
            r, g, b = hsv_to_rgb(hue, 1.0, 0.7)
            rgb_ext.pixels[i] = (r, g, b)

    def _animate_games(self, now):
        if game_reset_until and now >= game_reset_until:
            game_start_round()
        elif now - game_lit_at > GAME_TIMEOUT and not game_reset_until:
            game_reset_score()

    def _handle_game_press(self, sw):
        global game_score, game_reset_until

        if game_reset_until:
            return

        if sw == game_target:
            game_score += 1
            show_text_mode("GAMES", "Score: {}".format(game_score))
            game_start_round()
        else:
            game_reset_score()
            show_text_mode("GAMES", "Miss! Reset")


status = HackPadStatus()
keyboard.modules.append(status)

if __name__ == "__main__":
    keyboard.go()