import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

class KeyCoder:
    def __init__(self):
        self.kbd = Keyboard(usb_hid.devices)
        self.cc = ConsumerControl(usb_hid.devices)
        self.special_keys = {
            ' ': 'SPACE',
            '.': 'PERIOD',
            ',': 'COMMA',
            ';': 'SEMICOLON',
            "'": 'APOSTROPHE',
            '[': '0x2F',
            ']': '0x30',
            '-': 'MINUS',
            '=': 'EQUALS',
            '\\': 'BACKSLASH',
            '`': 'GRAVE_ACCENT',
            'INS': 'INSERT',
            'HOME': 'HOME',
            'PGUP': 'PAGE_UP',
            'PGDOWN': 'PAGE_DOWN',
            'END': 'END',
            '1': 'ONE',
            '2': 'TWO',
            '3': 'THREE',
            '4': 'FOUR',
            '5': 'FIVE',
            '6': 'SIX',
            '7': 'SEVEN',
            '8': 'EIGHT',
            '9': 'NINE',
            '0': 'ZERO',
            'Num0': 'KEYPAD_ZERO',
            'Num1': 'KEYPAD_ONE',
            'Num2': 'KEYPAD_TWO',
            'Num3': 'KEYPAD_THREE',
            'Num4': 'KEYPAD_FOUR',
            'Num5': 'KEYPAD_FIVE',
            'Num6': 'KEYPAD_SIX',
            'Num7': 'KEYPAD_SEVEN',
            'Num8': 'KEYPAD_EIGHT',
            'Num9': 'KEYPAD_NINE',
            'F1': '0x3A',
            'F2': '0x3B',
            'F3': '0x3C',
            'F4': '0x3D',
            'F5': '0x3E',
            'F6': '0x3F',
            'F7': '0x40',
            'F8': '0x41',
            'F9': '0x42',
            'F10': '0x43',
            'F11': '0x44',
            'F12': '0x45',
            'F13': '0x68',
            'F14': '0x69',
            'F15': '0x6A',
            'F16': '0x6B',
            'F17': '0x6C',
            'F18': '0x6D',
            'F19': '0x6E',
            'F20': '0x6F',
            'F21': '0x70',
            'F22': '0x71',
            'F23': '0x72',
            'F24': '0x73',
            'RIGHT_ARROW': '0x4F',
            'LEFT_ARROW': '0x50',
            'DOWN_ARROW': '0x51',
            'UP_ARROW': '0x52'
        }

        self.shift_special_keys = {
            '!': 'ONE',
            '@': 'TWO',
            '#': 'THREE',
            '$': 'FOUR',
            '%': 'FIVE',
            '^': 'SIX',
            '&': 'SEVEN',
            '*': 'EIGHT',
            '(': 'NINE',
            ')': 'ZERO',
            '_': 'MINUS',
            '+': 'EQUALS',
            '{': 'LEFT_BRACKET',
            '}': 'RIGHT_BRACKET',
            ':': 'SEMICOLON',
            '"': 'APOSTROPHE',
            '<': 'COMMA',
            '>': 'PERIOD',
            '?': 'SLASH',
            '|': 'BACKSLASH',
            '~': 'GRAVE_ACCENT'
        }
  
        self.media_keys = {
            'PLAY': ConsumerControlCode.PLAY_PAUSE,
            'PAUSE': ConsumerControlCode.PLAY_PAUSE,
            'VOLUP': ConsumerControlCode.VOLUME_INCREMENT,
            'VOLDOWN': ConsumerControlCode.VOLUME_DECREMENT,
            'SKIP': ConsumerControlCode.SCAN_NEXT_TRACK,
            'BACKSKIP': ConsumerControlCode.SCAN_PREVIOUS_TRACK,
            'STOP': ConsumerControlCode.STOP,
            'EJECT': ConsumerControlCode.EJECT,
            'FAST_FORWARD': ConsumerControlCode.FAST_FORWARD,
            'REWIND': ConsumerControlCode.REWIND,
            'MUTE': ConsumerControlCode.MUTE,
            'BRIGHTNESSUP': ConsumerControlCode.BRIGHTNESS_INCREMENT,
            'BRIGHTNESSDOWN': ConsumerControlCode.BRIGHTNESS_DECREMENT
        }

    def press_and_release_key(self, key, shift=False, alt=False, ctrl=False, rightS=False, rightA=False, rightC=False):
        if key in self.special_keys:
            for key_i, value_i in self.special_keys.items():
                if key == key_i: key = value_i       
        if key in self.shift_special_keys:
            shift = True
            for key_i, value_i in self.shift_special_keys.items():
                if key == key_i: key = value_i
   
        if shift: self.kbd.press(Keycode.RIGHT_SHIFT if rightS else Keycode.LEFT_SHIFT)
        if alt: self.kbd.press(Keycode.RIGHT_ALT if rightA else Keycode.LEFT_ALT)
        if ctrl: self.kbd.press(Keycode.RIGHT_CONTROL if rightC else Keycode.LEFT_CONTROL)
        
        if isinstance(key, str) and key.startswith('0x'):
            self.kbd.press(int(key, 16))
            self.kbd.release(int(key, 16))
        else:
            self.kbd.press(getattr(Keycode, key.upper()))
            self.kbd.release(getattr(Keycode, key.upper()))

        if shift or ctrl or alt:
            self.kbd.release(Keycode.RIGHT_SHIFT if rightS else Keycode.LEFT_SHIFT)
            self.kbd.release(Keycode.RIGHT_ALT if rightA else Keycode.LEFT_ALT)
            self.kbd.release(Keycode.RIGHT_CONTROL if rightC else Keycode.LEFT_CONTROL)
    
    def press_key(self, key):
        if "ctrl" in key: key = key.replace("ctrl", "control")
        if isinstance(key, str) and key.startswith('0x'):
            self.kbd.release(int(key, 16))
        else:
            self.kbd.press(getattr(Keycode, key.upper()))
            
    def release_key(self, key):
        if "ctrl" in key: key = key.replace("ctrl", "control")
        if isinstance(key, str) and key.startswith('0x'):
            self.kbd.release(int(key, 16))
        else:
            self.kbd.release(getattr(Keycode, key.upper()))
     
    def get_macro_steps(self, text):
        return text.split("+")

    def execute_step(self, section, state):
        wait_seconds = 0
        calr = ["shift", "alt", "ctrl",
                "left_shift", "left_alt", "left_ctrl",
                "right_shift", "right_alt", "right_ctrl"]

        if section.startswith('key<') and section.endswith('>'):
            key = section[4:-1]
            if key.lower() in calr:
                if "shift" in key.lower():
                    state['shift'] = True
                    if key.startswith("right"): state['rightS'] = True
                if "ctrl" in key.lower():
                    state['ctrl'] = True
                    if key.startswith("right"): state['rightC'] = True
                if "alt" in key.lower():
                    state['alt'] = True
                    if key.startswith("right"): state['rightA'] = True
            else:
                self.press_and_release_key(key, 
                    shift=state['shift'], alt=state['alt'], ctrl=state['ctrl'], 
                    rightS=state['rightS'], rightC=state['rightC'], rightA=state['rightA'])
                state.update({'ctrl': False, 'shift': False, 'alt': False, 
                             'rightC': False, 'rightS': False, 'rightA': False})
        
        elif section.startswith('press<') and section.endswith('>'):
            key = section[6:-1]
            self.press_key(key)
            
        elif section.startswith('release<') and section.endswith('>'):
            key = section[8:-1]
            self.release_key(key)
            
        elif section.startswith('text<') and section.endswith('>'):
            text = section[5:-1]
            for char in text:
                temp_shift, temp_alt, temp_rightA = state['shift'], state['alt'], state['rightA']
                if char in "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ":
                    char = char.replace("ą", "a").replace("ć", "c").replace("ę", "e").replace("ł", "l").replace("ń", "n").replace("ó", "o").replace("ś", "s").replace("ź", "z").replace("ż", "z").replace("Ą", "A").replace("Ć", "C").replace("Ę", "E").replace("Ł", "L").replace("Ń", "N").replace("Ó", "O").replace("Ś", "S").replace("Ź", "Z").replace("Ż", "Z")
                    temp_alt = True
                    temp_rightA = True
                if char.isupper():
                    temp_shift = True
                self.press_and_release_key(char, 
                    shift=temp_shift, alt=temp_alt, ctrl=state['ctrl'], 
                    rightS=state['rightS'], rightC=state['rightC'], rightA=temp_rightA)
        
        elif section.startswith('wait<') and section.endswith('>'):
            wait_val = section[5:-1]
            wait_seconds = float(wait_val.replace(",",".")) / 10
            
        elif section.startswith('media<') and section.endswith('>'):
            media_cmd = section[6:-1].upper()
            if media_cmd.startswith('VOLUP:'):
                vol = min(max(int(media_cmd[6:]), 1), 100)
                for _ in range(vol): self.cc.send(self.media_keys['VOLUP'])
            elif media_cmd.startswith('VOLDOWN:'):
                vol = min(max(int(media_cmd[8:]), 1), 100)
                for _ in range(vol): self.cc.send(self.media_keys['VOLDOWN'])
            elif media_cmd.startswith('BRIGHTNESSUP:'):
                br = min(max(int(media_cmd[13:]), 1), 100)
                for _ in range(br): self.cc.send(self.media_keys['BRIGHTNESSUP'])
            elif media_cmd.startswith('BRIGHTNESSDOWN:'):
                br = min(max(int(media_cmd[15:]), 1), 100)
                for _ in range(br): self.cc.send(self.media_keys['BRIGHTNESSDOWN'])
            else:
                self.cc.send(self.media_keys[media_cmd])
        
        return wait_seconds

    def finalize_macro(self, state):
        if state['shift']: self.release_key("left_shift")
        if state['shift'] and state['rightS']: self.release_key("right_shift")
        if state['ctrl']: self.release_key("left_ctrl")
        if state['ctrl'] and state['rightC']: self.release_key("right_ctrl")
        if state['alt']: self.release_key("left_alt")
        if state['alt'] and state['rightA']: self.release_key("right_alt")

    def send_and_decode(self, text):
        state = {'ctrl': False, 'shift': False, 'alt': False, 
                 'rightC': False, 'rightS': False, 'rightA': False}
        sections = self.get_macro_steps(text)
        for section in sections:
            wait = self.execute_step(section, state)
            if wait > 0: time.sleep(wait)
        self.finalize_macro(state)
        
    
def main():
    button1 = digitalio.DigitalInOut(board.GP16)
    button1.direction = digitalio.Direction.INPUT
    button1.pull = digitalio.Pull.UP
    
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    
    kc = KeyCoder()
    while True:
        if not button1.value:
            led.value = True
            kc.send_and_decode("wait<1.5>+key<a>")        
            time.sleep(0.25)
        else:
            led.value = False
    
if __name__ == "__main__": main()
