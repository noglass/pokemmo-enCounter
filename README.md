# PokeMMO enCounter
![screenshot](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot.png)  
![screenshot2](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot2.png)  
![screenshot3](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot3.png)  

enCounter is an extremely lightweight and cross-platform Python3 script that creates a floating widget window that will count your encounters in PokeMMO!  

This script works a bit differently than the existing ones, the main difference is that this does not use any sort of screen capturing to count the encounters!  
Instead, this lets you configure what key you have set to activate Sweet Scent and how many Pokemon are in each horde (you can set this to 1 for single shunting).  

There are also manual increment, decrement, horde increment (sweet scent), horde decrement, and undo buttons (and keybinds) for fine tuning.  

You can undo your last 50 actions. This includes resetting.  

You can pause the counter, disabling all key and button input, except for unpause and the exit button.

## Keybinds

Default:  
* Sweet Scent: `Unbound`
* Single Increment: `Ctrl+'+'` or `Ctrl+'='`
* Single Decrement: `Ctrl+'-'`
* Decrement By Horde Quantity: `Ctrl+'/'`
* Undo: `Ctrl+Z`
* Pause/Unpause: `Alt+Esc`
* Configuration Menu: `Ctrl+Esc`
* Reset Count: `Unbound`

All of these bindings can be held to repeat the task.  
Holding your Sweet Scent key will *not* repeatedly increment!  

All of these commands can now be bound to whatever key combos you like in the interactive configuration menu!

You can click and drag anywhere on the window to move it.  
The script will remember where you moved it to the next time you open it.

## Translations
Current translations:
* English (en)
* Chinese (cn) by [TheKingOfGlory](https://github.com/TheKingOfGlory)

Language specs can be added using the built-in `gettext` system.  
The `./locales/base.pot` file is a template file you can use to create new translations in the format of `./locales/{language}/LC_MESSAGES/base.po`, then run the `msgfmt` tool to compile the `./locales/{language}/LC_MESSAGES/base.mo` file, where `{language}` is the two letter abbreviation for the spec.  

When launching `counter.py` it attempts to select the language defined by your system, if a language spec exists for that language, it will be used. Otherwise it will fallback to English.  

If the automatic language detection doesn't work you can press the settings button, `⚙`, and select your preferred language.

## Themes
Now the `encounters.py` file supports customized color options!

## Dependencies
* pynput: `pip3 install pynput`
* tkinter: `sudo apt-get install python3-tk`
