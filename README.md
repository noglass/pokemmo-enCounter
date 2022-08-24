# PokeMMO enCounter
![screenshot](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot.png)  
![screenshot2](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot2.png)  
![screenshot3](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot3.png)  

enCounter is an extremely lightweight and cross-platform Python3 script that creates a floating widget window that will count your encounters in PokeMMO!  

This script works a bit differently than the existing ones, the main difference is that this does not use any sort of screen capturing to count the encounters!  
Instead, this lets you configure what key you have set to activate Sweet Scent and how many Pokemon are in each horde (you can set this to 1 for single shunting).  

There are also manual increment, decrement, horde increment, horde decrement, and undo buttons (and keybinds) for fine tuning.  

You can undo your last 50 actions. This includes resetting.  

You can pause the counter, disabling all key and button input, except for unpause and the exit button.

## Keybinds

Default:  
* Single Increment: `Ctrl+'+'` or `Ctrl+'='`
* Increment By Horde Quantity: `Ctrl+'*'` or `Ctrl+8`
* Single Decrement: `Ctrl+'-'`
* Decrement By Horde Quantity: `Ctrl+'/'`
* Undo (Up To the Last 50 Actions): `Ctrl+Z`
* Pause/Unpause: `Alt+Esc`
* Configure Sweet Scent Key and Horde Quantity: `Ctrl+Esc`
* Configure Only Horde Quantity: `Ctrl+H`

All of these bindings can be held to repeat the task.  
Holding your Sweet Scent key will *not* repeatedly increment!  

All of these commands (and more) can now be bound to whatever key combos you like in the interactive GUI!

You can click and drag anywhere on the window to move it.  
The script will remember where you moved it to the next time you open it.

## Translations
Current translations:
* English (en)
* Chinese (cn) by [TheKingOfGlory](https://github.com/TheKingOfGlory)

Language specs can be added using the built-in `gettext` system.  

When launching `counter.py` it attempts to select the language defined by your system, if a language spec exists for that language, it will be used. Otherwise it will fallback to English.  

If the automatic language detection doesn't work you can manually set the language in the generated `encounters.py` file:  

If you have the `encounters.py` file skip to step 5

1. Run `counter.py`
2. Press your sweet scent button, followed by a number.
3. Press the `+` button on the app.
4. Press the `X` to close the app.
5. Open the `encounters.py` file with any text editor (such as notepad)
6. Locate the line that says `langSet = None` and change it to `langSet = ['cn']`
7. Save and close the file.
8. Run `counter.py`

Now the app should be in Chinese! For other languages, just change the `cn` to the corresponding language abbreviation!

## Themes
Now the `encounters.py` file supports customized color options!

## Dependencies
* pynput: `pip3 install pynput`
* tkinter: `sudo apt-get install python3-tk`
