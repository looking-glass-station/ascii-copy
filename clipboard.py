import clipboard_monitor # windows only
import pyperclip

import ascii_clean

def print_text(text):
    new_text, changes = ascii_clean.normalize_text(text)

    pyperclip.copy(new_text)

if __name__ == '__main__':
    # windows only
    clipboard_monitor.on_update(print)
    clipboard_monitor.on_text(print_text)

    clipboard_monitor.wait()

