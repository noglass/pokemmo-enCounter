# PokeMMO enCounter
![screenshot](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot.png)  
![screenshot3](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot3.png)  
![screenshot4](https://raw.githubusercontent.com/noglass/pokemmo-enCounter/main/screenshot4.png)  

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

## Auto Launch With PokeMMO
If you are on Linux, you can modify the launch script to automatically launch enCounter on startup!  
If you are not on Linux, you can probably still accomplish this, but I just don't know how, sorry :(  

First locate your `pokemmo-installer` file, the location may vary depending on distro or desktop environment, mine was located at `/usr/games/pokemmo-installer` (Debian XFCE).  

Now open this file as root (or with `sudo`) and at the bottom you will find an `if-else` statement, right before the `if` statement paste the following code:  
```sh
DIRE=$PWD
cd /home/{user}/python/pokemmo-enCounter
./counter.py &
counter_pid=$!
cd $DIRE
```
Change the second line to the directory your `counter.py` file exists.  

Now inside the `else` statement add this line at the end, before the `fi`:  
```sh
	kill $counter_pid
```

If you got everything right, you should end up with this at the end of your file:  
```sh
DIRE=$PWD
cd /home/{user}/python/pokemmo-enCounter
./counter.py &
counter_pid=$!
cd $DIRE

if [[ $PKMO_CREATE_DEBUGS ]]; then
	cd "$POKEMMO"
    ( java ${JAVA_OPTS[*]} -cp PokeMMO.exe com.pokeemu.client.Client ) &

	client_pid=$!
	
	echo "DEBUG: Spawned client_pid $client_pid"
	
    rm -f "$POKEMMO/client_jvm.log"

    while :; do
        sleep 3
        kill -3 "$client_pid" || break
        echo "DEBUG: Threads dumped for Client JVM. Sleeping for 3 seconds.."
    done

	wait
else
	cd "$POKEMMO" && java ${JAVA_OPTS[*]} -cp PokeMMO.exe com.pokeemu.client.Client > /dev/null
	kill $counter_pid
fi
```

Now when you launch PokeMMO from your Applications launcher, it should automatically start enCounter!
