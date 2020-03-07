import tkinter as tk
import tkinter.font as font
from keyboard_listener import KeyboardListener, KeyWord
from replace_functions import replace, eval_replace
import json
import os
import threading
from pynput.keyboard import Key, Controller

### Threading ###

stop_event = threading.Event()
keyboard = Controller()

### Functions ###

def start_thread(target):
    stop_event.clear()
    thread = threading.Thread(target=target)
    thread.start()
    return thread
    
def get_font(family='Helvetica', size=14, weight='normal'):
    return font.Font(family=family, size=size, weight=weight)

def create_keywords_json():
    filename = 'keywords.json'
    with open(filename, 'a') as file:
        if os.path.getsize(filename) == 0:
            json.dump({}, file)

def update_keyword_json(new_keyword_text, new_value_text):
    filename = 'keywords.json'
    with open(filename) as file:
        keywords = json.load(file)

    keywords[new_keyword_text] = new_value_text
    with open(filename, 'w') as file:
        json.dump(keywords, file)

def convert_keywords_to_KeyWord_Objects():
    with open('keywords.json', 'r') as file:
        keywords = json.load(file)
    keyword_objects = {}
    for keyword, value in keywords.items():
        keyword_objects[keyword] = KeyWord(keyword, replace, keyword, value)
    return keyword_objects

def add_keyword_and_value():
    global keywords
    global keyboard_listener
    keyboard_listener.recent_input = []
    new_keyword_text = new_keyword.get()
    new_value_text = new_value.get("1.0", tk.END)
    # Remove newline that the text box randomly adds to the end of the string
    new_value_text = new_value_text[:-1]
    update_keyword_json(new_keyword_text, new_value_text)
    add_confirmation_label.config(text='Keyword Added')
    keywords = convert_keywords_to_KeyWord_Objects()
    keyboard_listener.keywords = keywords
    return keyboard_listener

def start_keyboard_listener():
    keyboard_listener = KeyboardListener(keywords=keywords)
    keyboard_listener_thread = start_thread(target=keyboard_listener.run)
    return keyboard_listener
    

### Setup ###

root = tk.Tk()

root.title("Keywordify")
root.wm_attributes("-topmost", 1)

# Create keywords.json if it doesn't already exist
create_keywords_json()

keywords = convert_keywords_to_KeyWord_Objects()

print(keywords)

### Styles ###

header_font = get_font('Arial', 16, 'bold')
text_font = get_font('Arial', 14)
button_font = get_font('Arial', 16)
alert_font = get_font('Arial', 11, 'bold')

### Frames ###

left_frame = tk.Frame(root, height=200, width=200)
left_frame.grid_propagate(0)

right_frame = tk.Frame(root, height=200, width=300)
# right_frame.grid_propagate(0)

### Labels ###

new_keyword_label = tk.Label(left_frame, text='New Keyword', font=header_font)
new_value_label = tk.Label(right_frame, text='New Keyword Value', font=header_font)
add_confirmation_label = tk.Label(left_frame, text='', font=alert_font, fg='green')

### Inputs ###

new_keyword = tk.Entry(left_frame, font=text_font)
new_value = tk.Text(right_frame, font=text_font, width=50, height=20)

### Buttons ###

create_keyword_btn = tk.Button(left_frame, text='Create', font=button_font, command=add_keyword_and_value)

### Layout ###

left_frame.grid(row=0, column=0, padx=5, pady=5)

new_keyword_label.grid(row=1, column=0)
new_keyword.grid(row=2, column=0, pady=(10,0))
create_keyword_btn.grid(row=3,column=0, sticky='nsew', pady=(10,0))
add_confirmation_label.grid(row=4, column=0, pady=(20,0))


right_frame.grid(row=0, column=1, padx=5, pady=5)

new_value_label.grid(row=0, column=0, sticky='nsew')
new_value.grid(row=1, column=0, pady=(10,0))

### Run Loop ###

keyboard_listener = start_keyboard_listener()

root.mainloop()
