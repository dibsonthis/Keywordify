from pynput.keyboard import Key, Listener, KeyCode
from functions import value, key_string, activate_special_key_if_pressed, deactivate_special_key_if_released, combo, current_key, is_special_key_pressed, release_all_special_keys

combos = {}
keywords = {}

class KeyboardListener:
    def __init__(self, combinations=combos, keywords=keywords):
        self.combos = combinations
        self.keywords = keywords
        self.keyboard_listener_thread = Listener(on_press=self.on_press, on_release=self.on_release)
        self.recent_input = []

    def on_press(self, key):
        key = key_string(key)
        global current_key
        global is_special_key_pressed
        # global recent_input
        self.recent_input.append(key)
        if len(self.recent_input) > 250:
            self.recent_input.pop(0)
        current_key = key
        activate_special_key_if_pressed(key)
        for combination in self.combos.values():
            if combo(combination, current_key):
                release_all_special_keys()
                combination.execute()
        for keyword in self.keywords.values():
            joined_recent_input = ''.join(self.recent_input)
            if keyword.joined_string_list in joined_recent_input:
                self.recent_input = []
                keyword.execute()
        

    def on_release(self, key):
        key = key_string(key)
        deactivate_special_key_if_released(key)
        if key == 'esc':
            return False

    def run(self, on_press = on_press, on_release = on_release):
        with self.keyboard_listener_thread as l:
            l.join()


class Combo:
    def __init__(self, special_keys, character, function, *args, **kwargs):
        self.special_keys = special_keys
        self.character = character
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def execute(self):
        self.function(*self.args, **self.kwargs)

class KeyWord:
    def __init__(self, string, function, *args, **kwargs):
        self.string = string
        self.string_list = ['space' if x == ' ' else x for x in self.string]
        self.joined_string_list = ''.join(self.string_list)
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def execute(self):
        self.function(*self.args, **self.kwargs)
