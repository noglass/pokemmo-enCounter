#!/bin/python3
# enCounter by MistressMuddy
# https://github.com/noglass/pokemmo-enCounter

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from sys import platform
import gettext
import copy
import threading

config = True
langSet = None
count = 0
quantity = 5
scentKey = None
setKey = False
last = [0] * 50
undoPoint = 0
modifier = False
altMod = False
shiftMod = False
superMod = False
pause = False
options = None
current = set()
theme = {
    'foreground': 'white',
    'background': 'grey',
    'activebackground': 'black',
    'activeforeground': 'white',
    'disabledforeground': '#A0A0A0',
    'pausedbackground': 'red',
    'updatebackground': 'yellow'
}

def applyTheme(obj,full=False):
    if full:
        obj.configure(fg=theme['foreground'], bg=theme['background'], activeforeground=theme['activeforeground'], activebackground=theme['activebackground'], disabledforeground=theme['disabledforeground'])
    else:
        obj.configure(fg=theme['foreground'], bg=theme['background'])

try:
    from encounters import *
except Exception as e:
    from pynput import keyboard
    wingeo = '+10+20'
    config = False
    scentKey      = [[]]
    plusKey       = [[keyboard.Key.ctrl,'+'],[keyboard.Key.ctrl,'=']]
    minusKey      = [[keyboard.Key.ctrl,'-']]
    minusHordeKey = [[keyboard.Key.ctrl,'/']]
    undoKey       = [[keyboard.Key.ctrl,'z']]
    configKey     = [[keyboard.Key.ctrl,keyboard.Key.esc]]
    pauseKey      = [[keyboard.Key.alt,keyboard.Key.esc]]
    resetKey      = [[]]

kbc = keyboard.Controller()

class Combo:
    def __init__(self, keys, func=None, name=None):
        self.keys = copy.deepcopy(keys)
        self.func = func
        self.name = name
        self.enabled = True
        self.len = len(keys)
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def match(self, keycombo):
        global options, pause
        if self.enabled and options == None and (pause == False or self.name == "pauseKey"):
            curlen = len(keycombo)
            if self.len == curlen and len(keycombo.intersection(self.keys)) == self.len:
                if self.func != None:
                    if self.len == 1 and self.name == "scentKey":
                        self.disable()
                    self.func(self)
                return True
        return False
    
    def write(self, file):
        foo = False
        file.write('[')
        for key in self.keys:
            if key == None:
                continue
            if foo:
                file.write(',')
            try:
                file.write(f"'{key.char}'")
            except AttributeError:
                file.write(f"keyboard.{key}")
            foo = True
        file.write(']')
    
    def to_str(self):
        foo = False
        out = ""
        for key in self.keys:
            if key == None:
                continue
            if foo:
                out += "+"
            try:
                out += str(key.char)
            except AttributeError:
                out += str(key)[4:]
            foo = True
        return out

if langSet == None:
    try:
        lang = gettext.translation('base', localedir='locales')
    except Exception as e:
        lang = gettext.translation('base', localedir='locales', languages=['en'])
else:
    langSet = None
    lang = gettext.translation('base', localedir='locales', languages=[langSet])

lang.install()
_ = lang.gettext

globalFont = ( "Verdana", 9, "normal" )

# CreateToolTip by crxguy52
# https://stackoverflow.com/a/36221216
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_attributes("-topmost", True)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength, font=globalFont)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
    
    def setText(self,text):
        self.text = text

def close():
    root.destroy()
    listener.stop()

lastClick = None

def onClick(event):
    global lastClick
    lastClick = [ event.x, event.y, 0 ]

def onDrag(event):
    global lastClick
    lastClick[2] = 1
    delta = [ event.x - lastClick[0], event.y - lastClick[1] ]
    root.geometry(f'+{root.winfo_x()+delta[0]}+{root.winfo_y()+delta[1]}')

def onUnClick(event):
    global lastClick
    if lastClick != None:
        if lastClick[2] == 1:
            save()
    lastClick = None

def incHorde(bind=None):
    inc(bind,quantity)

def decHorde(bind=None):
    dec(bind,quantity)

def undo(bind=None):
    global count, last, undoPoint, undoButton
    if undoPoint > 0 or last[undoPoint] != 0:
        count += last[undoPoint]
        undoPoint -= 1
        if undoPoint < 0:
            undoPoint = 0
            last[undoPoint] = 0
        if undoPoint == 0 and last[undoPoint] == 0:
            undoButton["state"] = "disabled"
        save()

def togglePause(bind=None):
    global pause, plusButton, minusButton, undoButton, configButton, resetButton
    pause = not pause
    if pause:
        label.config(text=_('PAUSED'))
        labeltip.setText(_('Input is being paused!'))
        plusButton["state"] = "disabled"
        minusButton["state"] = "disabled"
        undoButton["state"] = "disabled"
        configButton["state"] = "disabled"
        resetButton["state"] = "disabled"
        setColor(theme['pausedbackground'])
    else:
        displayCount()
        plusButton["state"] = "normal"
        minusButton["state"] = "normal"
        configButton["state"] = "normal"
        resetButton["state"] = "normal"
        if undoPoint > 0 or last[undoPoint] != 0:
            undoButton["state"] = "normal"
        resetColor()
    root.update()

def displayCount():
    label.config(text='{:,}'.format(count))
    foo = False
    key = ""
    for k in keyBindings:
        if k.name == "scentKey":
            if foo:
                key += " or "
            key += k.to_str()
            foo = True
    labeltip.setText(f"{_('Horde quantity')}: {quantity}\n{_('Sweet Scent Key')}: {key}")
    setColor(theme['updatebackground'])
    threading.Timer(0.02,resetColor).start()

def inc(bind=None,n=1):
    global count, last, undoPoint, undoButton
    count += n
    undoPoint += 1
    if undoPoint > 49:
        last.pop(0)
        last.append(n*-1)
        undoPoint = 49
    else:
        last[undoPoint] = n*-1
    if undoButton["state"] == "disabled":
        undoButton["state"] = "normal"
    save()

def dec(bind=None,n=1):
    global count, last, undoPoint, undoButton
    count -= n
    undoPoint += 1
    if undoPoint > 49:
        last.pop(0)
        last.append(n)
        undoPoint = 49
    else:
        last[undoPoint] = n
    if undoButton["state"] == "disabled":
        undoButton["state"] = "normal"
    save()

def reset(bind=None):
    dec(bind,count)

cmdNames = ['scentKey', 'plusKey', 'minusKey', 'minusHordeKey', 'undoKey', 'configKey', 'pauseKey', 'resetKey']
cmdDisplay = [_('Sweet Scent'), _('Increment'), _('Decrement'), _('Horde Decrement'), _('Undo'), _('Settings'), _('Pause'), _('Reset')]
displayLength = 0
for i in cmdDisplay:
    j = len(i)
    if j > displayLength:
        displayLength = j
displayLength += 1
keylist = None
binds = None
tempBindings = None
userCombo = None
keybtn = None

def configure(bind=None,scent=False):
    global pause, options, keylist, binds, tempBindings, keyBindings, pauseButton
    if options != None:
        return
    pause = False
    togglePause()
    pauseButton["state"] = "disabled"
    
    binds = list()
    tempBindings = list()
    
    options = tk.Toplevel(root)
    options.title(_('enCounter Settings'))
    
    def popList():
        global keylist, binds, tempBindings
        binds = list()
        tempBindings = list()
        for b in keyBindings:
            name = cmdDisplay[cmdNames.index(b.name)]
            binds.append(f"{name}:{' ' * (displayLength - len(name))}{b.to_str()}")
            tempBindings.append(b)
        if keylist == None:
            keylist = tk.StringVar(value=binds)
        else:
            keylist.set(binds)
    
    popList()
    tk.Label(options, text=_('Horde Count: '), font=globalFont).grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    hordesv = tk.StringVar(value=f'{quantity}')
    hordesv.trace("w", lambda name, index, mode, hordesv=hordesv: on_edit(hordesv))
    hordeBox = tk.Entry(options, textvariable=hordesv, font=globalFont, width=2)
    hordeBox.grid(row=3, column=1, pady=5, sticky=tk.W)
    bindlist = tk.Listbox(options, listvariable=keylist, width=37, height=10, selectmode='browse', font=("monospace", 9, "normal"))
    bindlist.grid(row=1, column=0, columnspan=3, sticky=tk.E+tk.W)
    
    listScrollX = tk.Scrollbar(options, orient=tk.HORIZONTAL, command=bindlist.xview)
    listScrollY = tk.Scrollbar(options, orient=tk.VERTICAL, command=bindlist.yview)
    listScrollX.grid(row=2, columnspan=3, sticky=tk.E+tk.W)
    listScrollY.grid(row=1, column=3, sticky=tk.N+tk.S)
    bindlist['xscrollcommand'] = listScrollX.set
    bindlist['yscrollcommand'] = listScrollY.set
    
    addbtn = tk.Button(options, text=_('Add'), font=globalFont)
    delbtn = tk.Button(options, text=_('Remove'), font=globalFont)
    savebtn = tk.Button(options, text=_('Save'), font=globalFont)
    savebtn["state"] = "disabled"
    delbtn["state"] = "disabled"
    addbtn.grid(row=0, column=0, columnspan=2, pady=5)
    delbtn.grid(row=0, column=1, columnspan=2, pady=5)
    savebtn.grid(row=3, column=2, pady=5, sticky=tk.E)
    
    def closeOptions():
        global pause, options, tempBindings, binds, keylist
        options.destroy()
        options.update()
        options = None
        tempBindings = None
        binds = None
        keylist = None
        pause = True
        togglePause()
        pauseButton["state"] = "normal"
    
    def on_edit(sv=None):
        nonlocal savebtn
        savebtn["state"] = "normal"
    
    def on_select(event=None):
        nonlocal delbtn
        delbtn["state"] = "normal"
    
    bindlist.bind('<<ListboxSelect>>',on_select)
    
    
    def on_save():
        global quantity, tempBindings, keyBindings
        try:
            quantity = int(hordeBox.get())
            keyBindings.clear()
            #for k in tempBindings:
            #    keyBindings.add(k)
            keyBindings = set(copy.deepcopy(tempBindings))
            save()
            messagebox.showinfo(_("Success!"), _("Configuration saved!"), parent=options)
            closeOptions()
        except ValueError:
            messagebox.showerror(_("Error"), _("Horde count must be a valid number!"), parent=options)
    
    def on_delete():
        global binds, tempBindings
        nonlocal delbtn
        i = bindlist.curselection()
        if len(i) > 0:
            i = i[0]
            del binds[i]
            del tempBindings[i]
            keylist.set(binds)
            on_edit()
        else:
            delbtn["state"] = "disabled"
    
    def on_add(scent=False):
        nonlocal hordeBox, addbtn, delbtn, bindlist
        global setKey, keybtn
        def on_keyPrompt(event=None):
            global setKey
            keybtn.configure(text=_('Press a key . . .'))
            setKey = True
        def on_newBind():
            n = cmdDisplay.index(cmdbox.get())
            userCombo.func = callback[n]
            userCombo.name = cmdNames[n]
            binds.append(f"{cmdDisplay[n]}:{' ' * (displayLength - len(cmdDisplay[n]))}{userCombo.to_str()}")
            tempBindings.append(copy.deepcopy(userCombo))
            keylist.set(binds)
            on_edit()
            closePrompt()
        def closePrompt():
            hordeBox["state"] = "normal"
            addbtn["state"] = "normal"
            if len(bindlist.curselection()) > 0:
                delbtn["state"] = "normal"
            bindlist["state"] = "normal"
            prompt.destroy()
            prompt.update()
        
        prompt = tk.Toplevel(options)
        prompt.title(_("Create"))
        hordeBox["state"] = "disabled"
        addbtn["state"] = "disabled"
        delbtn["state"] = "disabled"
        bindlist["state"] = "disabled"
        tk.Label(prompt, text=_("Command:")).grid(row=0,column=0,padx=5,pady=5)
        cmdopt = tk.StringVar()
        #cmdopt.trace('w',on_keyPrompt)
        cmdbox = ttk.Combobox(prompt, textvariable=cmdopt)
        cmdbox.bind('<<ComboboxSelected>>',on_keyPrompt)
        cmdbox['values'] = cmdDisplay
        cmdbox.grid(row=1,column=0,padx=5,pady=5)
        #tk.Label(prompt, text="Key Bind:").grid(row=2,column=0,padx=5,pady=5)
        keybtn = tk.Button(prompt, text=_('Assign Key'), command=on_keyPrompt)
        keybtn.grid(row=2,column=0,columnspan=2,padx=5,pady=5)
        okaybtn = tk.Button(prompt, text='Okay', padx=5, pady=5, command=on_newBind)
        okaybtn.grid(row=3,column=0,columnspan=2, padx=15, pady=5)
        prompt.protocol("WM_DELETE_WINDOW", closePrompt)
        #prompt.wm_attributes("-topmost" , -1)
        #prompt.after(1, lambda: prompt.focus_force())
        if scent:
            cmdbox.set(cmdDisplay[0])
            cmdbox.current(0)
            messagebox.showinfo(_("Attention"), _("Please assign your Sweet Scent Key!"), parent=prompt)
            prompt.wm_attributes("-topmost" , -1)
            #prompt.after(1, lambda: prompt.focus_force())
        cmdbox.configure(state='readonly')
    
    
    
    addbtn.configure(command=on_add)
    delbtn.configure(command=on_delete)
    savebtn.configure(command=on_save)
    
    if scent:
        on_add(scent)
    
    def on_close():
        if savebtn["state"] == "disabled" or messagebox.askokcancel(_("Close"), _("Configuration has not been saved! Discard changes?"), parent=options):
            closeOptions()
            return False
        return True
    options.protocol("WM_DELETE_WINDOW", on_close)

callback = [incHorde,inc,dec,decHorde,undo,configure,togglePause,reset]

def setColor(color):
    root.configure(bg=color)
    holder.configure(bg=color)
    label.configure(bg=color)
    plusButton.configure(bg=color)
    minusButton.configure(bg=color)
    configButton.configure(bg=color)
    resetButton.configure(bg=color)
    pauseButton.configure(bg=color)
    undoButton.configure(bg=color)
    exitButton.configure(bg=color)

def resetColor():
    setColor(theme['background'])

root = tk.Tk()
root.attributes('-topmost', True)
root.overrideredirect(True)
root.title(_('enCounter'))
root.resizable(False, False)
#root.attributes('-alpha', 0.5)
root.configure(bg=theme['background'])
root.bind('<ButtonPress-1>', onClick)
root.bind('<ButtonRelease-1>', onUnClick)
root.bind('<B1-Motion>', onDrag)

def save():
    file = open('encounters.py', 'w')
    file.write(f"""#!/bin/python3
from pynput import keyboard

# For Chinese use:
# langSet = 'cn'
langSet = {langSet}
quantity = {quantity}
count = {count}
wingeo = "+{root.winfo_x()}+{root.winfo_y()}"

# Key Bindings:
""")
    for n in cmdNames:
        file.write(f'{n} = [')
        foo = False
        for b in keyBindings:
            if b.name == n:
                if foo:
                    file.write(',')
                b.write(file)
                foo = True
        file.write(']\n')
    file.write('\n# Theme Settings:\ntheme = {\n')
    foo = False
    for k, v in theme.items():
        if foo:
            file.write(',\n')
        file.write(f"    '{k}': '{v}'")
        foo = True
    file.write('\n}\n')
    file.close()
    if not pause:
        displayCount()
    root.update()

if platform == 'win32' or platform == 'cygwin':
    holder = tk.Label(text='', font=( "Verdana", 12, "normal" ))
    exitButton = tk.Button(text='×', width=2, command=close, font=globalFont)
    label = tk.Label(text='{:,}'.format(count), font=globalFont)
    plusButton = tk.Button(text='+', width=2, command=inc, font=globalFont)
    minusButton = tk.Button(text='-', width=2, command=dec, font=globalFont)
    undoButton = tk.Button(text=_('Undo'), width=6, command=undo, font=globalFont)
    configButton = tk.Button(text='⚙', width=2, command=configure, font=globalFont)
    pauseButton = tk.Button(text='⏸︎', width=2, command=togglePause, font=globalFont)
    resetButton = tk.Button(text=_('Reset'), width=6, command=reset, font=globalFont)
else:
    pixelVirtual = tk.PhotoImage(width=1, height=1)
    holder = tk.Label(text='', font=globalFont)
    exitButton = tk.Button(text='×', image=pixelVirtual, width=3, height=6, compound='c', command=close, font=globalFont)
    label = tk.Label(text='', font=globalFont)
    plusButton = tk.Button(text='+', image=pixelVirtual, width=3, height=6, compound='c', command=inc, font=globalFont)
    minusButton = tk.Button(text='-', image=pixelVirtual, width=3, height=6, compound='c', command=dec, font=globalFont)
    undoButton = tk.Button(text=_('Undo'), image=pixelVirtual, width=25, height=6, compound='c', command=undo, font=globalFont)
    configButton = tk.Button(text='⚙', image=pixelVirtual, width=3, height=6, compound='c', command=configure, font=globalFont)
    pauseButton = tk.Button(text='⏸︎', image=pixelVirtual, width=3, height=6, compound='c', command=togglePause, font=globalFont)
    resetButton = tk.Button(text=_('Reset'), image=pixelVirtual, width=25, height=6, compound='c', command=reset, font=globalFont)

applyTheme(holder)
applyTheme(label)
applyTheme(exitButton,True)
applyTheme(plusButton,True)
applyTheme(minusButton,True)
applyTheme(undoButton,True)
applyTheme(configButton,True)
applyTheme(pauseButton,True)
applyTheme(resetButton,True)

CreateToolTip(exitButton,_('Exit'))
labeltip = CreateToolTip(label,'')
plusTip = CreateToolTip(plusButton,_("Increase count"))
minusTip = CreateToolTip(minusButton,_("Decrease count"))
CreateToolTip(undoButton,_('Undo the last action'))
CreateToolTip(configButton,_('Configure'))
CreateToolTip(pauseButton,_('Pause'))
CreateToolTip(resetButton,_('Reset your count to 0.\nCan be undone!'))

holder.grid(row=0, column=2)
label.place(x=0,y=0)
plusButton.grid(row=1, column=0, sticky='w', ipadx=0)
minusButton.grid(row=1, column=1, sticky='w', ipadx=0)
undoButton.grid(row=1, column=2, sticky='w', ipadx=0)
configButton.grid(row=2, column=0, sticky='w', ipadx=0)
pauseButton.grid(row=2, column=1, sticky='w', ipadx=0)
resetButton.grid(row=2, column=2, sticky='w', ipadx=0)

root.update_idletasks()
winWidth = root.winfo_width()
exitButton.place(x=winWidth-exitButton.winfo_reqwidth(),y=0)

undoButton["state"] = "disabled"

exitWidth = exitButton.winfo_reqwidth()

def resizeToFit(width = winWidth-exitWidth):
    root.geometry(f'{width+exitWidth}x{root.winfo_height()}')
    exitButton.place(x=width,y=0)

root.geometry(wingeo)

keyBindings = set()

def sortKeys(c):
    k = str(c)[4:]
    try:
        return ["shift","ctrl","alt","cmd"].index(k)
    except ValueError:
        if len(k) < 1:
            return 4 + ord(str(c.char))
    return 4 + ord(k[0])
            

def linkBindings():
    bindings = [scentKey,plusKey,minusKey,minusHordeKey,undoKey,configKey,pauseKey,resetKey]
    i = 0
    for bind in bindings:
        if len(bind) > 0:
            for combo in bind:
                if len(combo) > 0:
                    keys = list()
                    for key in combo:
                        if isinstance(key,str):
                            key = keyboard.KeyCode(char=key)
                        keys.append(key)
                        keys.sort(key=sortKeys)
                    keyBindings.add(Combo(keys,callback[i],cmdNames[i]))
        i += 1
linkBindings()

if config == False:
    configure(None,True)

displayCount()

def on_press(key):
    global setKey, userCombo
    if key != None:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            key = keyboard.Key.ctrl
        elif key == keyboard.Key.alt_gr or key == keyboard.Key.alt_r or key == keyboard.Key.alt_l:
            key = keyboard.Key.alt
        elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            key = keyboard.Key.shift
        elif key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            key = keyboard.Key.cmd
        
        
        current.add(key)
        
        if not setKey:
            if key == keyboard.Key.ctrl:
                plusButton.configure(text=f'+{quantity}', command=incHorde)
                minusButton.configure(text=f'-{quantity}', command=decHorde)
                plusTip.setText(f"{_('Increase count by')} {quantity}")
                minusTip.setText(f"{_('Decrease count by')} {quantity}")
            
            for c in keyBindings:
                #if c.match(current) and c.name != 'pauseKey' and c.name != 'configKey':
                c.match(current)

def on_release(key):
    global setKey, userCombo, current, keyBindings
    if key != None:
        if setKey:
            userCombo = Combo(set(filter(None,current)))
            keybtn.configure(text=userCombo.to_str())
            setKey = False
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            key = keyboard.Key.ctrl
        elif key == keyboard.Key.alt_gr or key == keyboard.Key.alt_r or key == keyboard.Key.alt_l:
            key = keyboard.Key.alt
        elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            key = keyboard.Key.shift
        elif key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            key = keyboard.Key.cmd
        
        if key == keyboard.Key.ctrl:
            plusButton.configure(text='+', command=inc)
            minusButton.configure(text='-', command=dec)
            plusTip.setText(_('Increase count'))
            minusTip.setText(_('Decrease count'))
        
        activated = False
        
        for c in keyBindings:
            curlen = len(current)
            if c.name == "scentKey" and c.len == curlen and len(current.intersection(set(c.keys))) == c.len:
                act = c.enable()
                if not activated:
                    activated = act
        if not activated:
            current.clear()
    
    try:
        current.remove(key)
    except KeyError:
        current.clear()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    root.mainloop()
    listener.join()

