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
profile_led = None
keys_leds = None

###-###-###-### - Buttons Setup - ###-###-###-###
button0 = digitalio.DigitalInOut(board.GP16)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.UP

button1 = digitalio.DigitalInOut(board.GP17)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP18)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

button3 = digitalio.DigitalInOut(board.GP19)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

button4 = digitalio.DigitalInOut(board.GP20)
button4.direction = digitalio.Direction.INPUT
button4.pull = digitalio.Pull.UP

button5 = digitalio.DigitalInOut(board.GP21)
button5.direction = digitalio.Direction.INPUT
button5.pull = digitalio.Pull.UP

###-###-### - Control Led Setup - ###-###-###
pico_led = digitalio.DigitalInOut(board.LED)
pico_led.direction = digitalio.Direction.OUTPUT

###-###-###-###-### - Config Read - ###-###-###-###-###
if JsonTools().jsonVeryficator("binds_config.json"):
    if JsonTools().bindVeryficator("binds_config.json"):
        with open('binds_config.json') as f:
            profiles = json.load(f)
    else:
        raise OSError("Plik binds_config.json ma niepoprawną strukturę")
else:
    raise OSError("Plik binds_config.json jest uszkodzony")

###-###-###-###-###-### - Config Setup - ###-###-###-###-###-###
buttons = [button0, button1, button2, button3, button4, button5]
keys = ["key.0", "key.1", "key.2", "key.3", "key.4", "key.5"]

###-### - Read Last Profile - ###-###
selected_profile = "profile.0"

###-###-### - Main Loop - ###-###-###
while True:
    for i, button in enumerate(buttons):
        if not button.value:
            pico_led.value = True
            if "profile<" in profiles[selected_profile][keys[i]][0]:
                selected_profile = "profile." + profiles[selected_profile][keys[i]][0].split('<')[1].split('>')[0]
            else:
                KeyCoder().send_and_decode(profiles[selected_profile][keys[i]][0])
            time.sleep(0.25)
        else:
            pico_led.value = False