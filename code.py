import time
import board
import digitalio
import usb_hid
import json
from key_coder import KeyCoder
from json_reader import JsonTools

### - Base Config - ###
use_rgb = False

###-###-###-### - RGB Led Setup - ###-###-###-###
# TODO: Implement NeoPixel initialization
profile_led = None
keys_leds = None

###-###-###-### - Buttons Setup - ###-###-###-###
button_pins = [board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21]
buttons = []
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

###-###-### - Control Led Setup - ###-###-###
pico_led = digitalio.DigitalInOut(board.LED)
pico_led.direction = digitalio.Direction.OUTPUT

###-###-###-###-### - Config Read - ###-###-###-###-###
jt = JsonTools()
if jt.jsonVeryficator("binds_config.json"):
    if jt.bindVeryficator("binds_config.json"):
        with open('binds_config.json') as f:
            profiles = json.load(f)
    else:
        raise OSError("Plik binds_config.json ma niepoprawną strukturę")
else:
    raise OSError("Plik binds_config.json jest uszkodzony")

###-###-###-###-###-### - Config Setup - ###-###-###-###-###-###
keys = ["key.0", "key.1", "key.2", "key.3", "key.4", "key.5"]
kc = KeyCoder()

###-### - Read Last Profile - ###-###
selected_profile = "profile.0"

###-###-### - Macro Management - ###-###-###
last_press_times = [0.0] * len(buttons)
debounce_delay = 0.25
active_macros = {}

###-###-### - Main Loop - ###-###-###
while True:
    current_time = time.monotonic()
    
    for i, button in enumerate(buttons):
        if not button.value:
            if (current_time - last_press_times[i]) > debounce_delay:
                command_str = profiles[selected_profile][keys[i]][0]
                
                if "profile<" in command_str:
                    selected_profile = "profile." + command_str.split('<')[1].split('>')[0]
                else:
                    # TODO: Implement LED color change to press_color if use_rgb is True
                    press_color = profiles[selected_profile][keys[i]][1]
                    
                    active_macros[i] = {
                        "steps": kc.get_macro_steps(command_str),
                        "next_run": current_time,
                        "state": {'ctrl': False, 'shift': False, 'alt': False, 
                                 'rightC': False, 'rightS': False, 'rightA': False}
                    }
                
                last_press_times[i] = current_time

    finished_macros = []
    for macro_id, macro in active_macros.items():
        if current_time >= macro["next_run"]:
            if macro["steps"]:
                step = macro["steps"].pop(0)
                wait_time = kc.execute_step(step, macro["state"])
                macro["next_run"] = current_time + wait_time
            else:
                kc.finalize_macro(macro["state"])
                finished_macros.append(macro_id)

    for macro_id in finished_macros:
        del active_macros[macro_id]
        # TODO: Restore profile color

    any_button_held = any(not b.value for b in buttons)
    pico_led.value = bool(active_macros) or any_button_held
    
    time.sleep(0.001)
