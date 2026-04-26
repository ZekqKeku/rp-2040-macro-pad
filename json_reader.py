try:
    import json
    import os
    import re
except ImportError as e:
    print(f"\n\n  >> Błąd importu bibliotek: {e}\n\n")

class JsonTools():
    def __init__(self, class_path:str=""):
        self.class_path = class_path
    
    def relativeFilePath(self, target:str=None):
        if target is not None: 
            return f"{self.class_path}/{target}" if self.class_path else target
        else: 
            return self.class_path if self.class_path else "."

    def jsonVeryficator(self, file:str):
        try:
            with open(self.relativeFilePath(file), "r") as f: json.load(f)
            return True
        except (OSError, ValueError):
            return False

    def bindVeryficator(self, file:str):
        def is_hex_color(s):
            if len(s) not in (4, 7):
                return False
            try:
                int(s[1:], 16)
                return True
            except ValueError:
                return False

        prof = False
        with open(self.relativeFilePath(file), "r") as f: 
            data = json.load(f)
            for key, value in data.items():
                if isinstance(value, dict) and ("color" not in value or ("color" in value and not is_hex_color(value["color"]))):
                    return False
                for subkey, subvalue in value.items():
                    if subkey == "color":
                        continue
                    if subkey.startswith("key.") and isinstance(subvalue, list) and len(subvalue) == 2:
                        command, color = subvalue
                        commands = ["profile", "key", "press", "release", "text", "media"]
                        if not any(cmd in command for cmd in commands) or not command.endswith(">") or is_hex_color(color) == False:
                            return False
                    else:
                        return False
                prof = True
        return prof
    
    def hex_to_rgbc(self, hex_color):
        if hex_color[0] == '#': hex_color = hex_color[1:]
        r_val = int(hex_color[0:2], 16)
        g_val = int(hex_color[2:4], 16)
        b_val = int(hex_color[4:6], 16)
        return r_val, g_val, b_val

    def load_profile(self):
        try:
            with open('data.txt', 'r') as f:
                data = json.load(f)
                profile = data.get('profile', 0)
        except FileNotFoundError:
            profile = 0
            with open('data.txt', 'w') as f:
                json.dump({'profile': profile}, f)
        return profile

    def update_profile(self, profile):
        try:
            with open('data.txt', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data['profile'] = profile
        with open('data.txt', 'w') as f:
            json.dump(data, f)

def main():
    tool = JsonTools()

    print(tool.jsonVeryficator("binds_config.json"))
    print(tool.bindVeryficator("binds_config.json"))


if __name__ == "__main__": main()
