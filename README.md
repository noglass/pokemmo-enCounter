# PokeMMO enCounter
enCounter is an extremely lightweight and cross-platform  
Python3 script that creates a floating widget window that will  
count your encounters in PokeMMO!  

This script works a bit differently than the existing ones,  
the main difference is that this does not use any sort of  
screen capturing to count the encounters!  
Instead, this lets you configure what key you have set to  
activate Sweet Scent and how many Pokemon are in each horde  
(you can set this to 1 for single shunting).  

There are also manual increment, decrement, horde increment,  
horde decrement, and undo buttons (and keybinds) for fine tuning.  

You can undo your last 50 actions. This includes resetting.  

You can pause the counter, disabling all key and button input,  
except for unpause and the exit button.
![screenshot](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot.png)

## Keybinds
* Single Increment: `Ctrl+'+'` or `Ctrl+'='`
* Horde Quantity Increment: `Ctrl+'*'` or `Ctrl+8`
* Single Decrement: `Ctrl+'-'`
* Horde Decrement: `Ctrl+'/'`
* Undo: `Ctrl+Z`
* Pause/Unpause: `Alt+Esc`
* Configure Sweet Scent Key and Horde Quantity: `Ctrl+Esc`
* Configure Only Horde Quantity: `Ctrl+h`

All of these bindings can be held to repeat the task.  
Holding your Sweet Scent key will *not* repeatedly increment!
