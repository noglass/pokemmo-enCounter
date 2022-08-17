#!/bin/python3
# enCounter by MistressMuddy
# https://github.com/noglass/pokemmo-enCounter

import tkinter as tk
from sys import platform

globalFont = ( "Verdana", 9, "normal" )

# CreateToolTip by crxguy52
# https://stackoverflow.com/a/36221216
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='部件信息'):
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

count = 0
quantity = 5
scentKey = None
setKey = 0
last = [0] * 50
undoPoint = 0
modifier = False
altMod = False
shiftMod = False
superMod = False
pause = False

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

def plusOne():
    inc(1)

def minusOne():
    dec(1)

def undo():
    global count, last, undoPoint, undoButton
    count += last[undoPoint]
    undoPoint -= 1
    if undoPoint < 0:
        undoPoint = 0
        last[undoPoint] = 0
    if undoPoint == 0 and last[undoPoint] == 0:
        undoButton["state"] = "disabled"
    save()

def togglePause():
    global pause, plusButton, minusButton, undoButton, configButton, resetButton
    pause = not pause
    if pause:
        label.config(text='暂停中')
        labeltip.setText('程序正在暂停！\n按Alt+Esc继续！')
        plusButton["state"] = "disabled"
        minusButton["state"] = "disabled"
        undoButton["state"] = "disabled"
        configButton["state"] = "disabled"
        resetButton["state"] = "disabled"
        setColor('red')
    else:
        if count < 10:
            label.config(text='{:,} '.format(count))
        else:
            label.config(text='{:,}'.format(count))
        labeltip.setText(f'群怪数量： {quantity}\n甜甜香气按键： {scentKey}')
        plusButton["state"] = "normal"
        minusButton["state"] = "normal"
        configButton["state"] = "normal"
        resetButton["state"] = "normal"
        if undoPoint > 0 or last[undoPoint] != 0:
            undoButton["state"] = "normal"
        setColor('grey')
    root.update()

def configure(retry=False):
    global setKey
    if setKey == 0:
        label.config(text='请按下你的甜甜香气快捷键！')
        labeltip.setText('请按下您已经绑定的快捷键以激活甜甜香气')
    else:
        if retry:
            label.config(text='请输入每次群怪的个数！请输入有效数字！')
            setKey -= 1
        else:
            label.config(text='请输入每次群怪的次数！')
        labeltip.setText('输入一个与您每次群怪数量相等的数字')
    resizeToFit(label.winfo_reqwidth())
    root.update()
    setKey += 1

def reset():
    dec(count)

def setColor(color):
    root.configure(bg=color)
    label.configure(bg=color)
    plusButton.configure(bg=color)
    minusButton.configure(bg=color)
    configButton.configure(bg=color)
    resetButton.configure(bg=color)
    pauseButton.configure(bg=color)
    undoButton.configure(bg=color)
    exitButton.configure(bg=color)

root = tk.Tk()
root.attributes('-topmost', True)
root.overrideredirect(True)
root.title('enCounter')
root.resizable(False, False)
#root.attributes('-alpha', 0.5)
root.configure(bg='grey')
root.bind('<ButtonPress-1>', onClick)
root.bind('<ButtonRelease-1>', onUnClick)
root.bind('<B1-Motion>', onDrag)

if platform == 'win32' or platform == 'cygwin':
    tk.Label(text='', bg='grey', fg='white', font=( "Verdana", 12, "normal" )).grid(row=0, column=2)
    exitButton = tk.Button(text='×', width=2, command=close, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    label = tk.Label(text='{:,}'.format(count), bg='grey', fg='white', font=globalFont)
    plusButton = tk.Button(text='+', width=2, command=plusOne, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    minusButton = tk.Button(text='-', width=2, command=minusOne, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    undoButton = tk.Button(text='撤销', width=6, command=undo, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    configButton = tk.Button(text='⚙', width=2, command=configure, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    pauseButton = tk.Button(text='⏸︎', width=2, command=togglePause, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    resetButton = tk.Button(text='重置', width=6, command=reset, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
else:
    pixelVirtual = tk.PhotoImage(width=1, height=1)
    tk.Label(text='', bg='grey', fg='white', font=globalFont).grid(row=0, column=2)
    exitButton = tk.Button(text='×', image=pixelVirtual, width=3, height=6, compound='c', command=close, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    label = tk.Label(text='{:,}'.format(count), bg='grey', fg='white', font=globalFont)
    plusButton = tk.Button(text='+', image=pixelVirtual, width=3, height=6, compound='c', command=plusOne, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    minusButton = tk.Button(text='-', image=pixelVirtual, width=3, height=6, compound='c', command=minusOne, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    undoButton = tk.Button(text='撤销', image=pixelVirtual, width=25, height=6, compound='c', command=undo, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    configButton = tk.Button(text='⚙', image=pixelVirtual, width=3, height=6, compound='c', command=configure, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    pauseButton = tk.Button(text='⏸︎', image=pixelVirtual, width=3, height=6, compound='c', command=togglePause, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)
    resetButton = tk.Button(text='重置', image=pixelVirtual, width=25, height=6, compound='c', command=reset, bg='grey', fg='white', activebackground='black', activeforeground='white', font=globalFont)

CreateToolTip(exitButton,'Exit')
labeltip = CreateToolTip(label,f'Horde quantity: {quantity}\nSweet Scent Key: {scentKey}')
CreateToolTip(plusButton,"增加计数，按\nCtrl+'+' 或者 Ctrl+'='\n如按群怪数量增加计数，请按\nCtrl+'*' or Ctrl+8")
CreateToolTip(minusButton,"减少计数，按\nCtrl+'-'\n如按群怪数量减少计数，请按\nCtrl+'/'")
CreateToolTip(undoButton,'Ctrl+Z')
CreateToolTip(configButton,'设置\nCtrl+Esc')
CreateToolTip(pauseButton,'暂停\nAlt+Esc')
CreateToolTip(resetButton,'点击此按钮可将计数重置为0\n可以撤销 ;p')

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

try:
    from encounters import *
except Exception as e:
    from pynput import keyboard
    setKey = 1
    wingeo = '+10+20'
    label.config(text='请按下您的甜甜香气快捷键！')
    labeltip.setText('按下您已绑定的按键以激活甜甜香气')
    resizeToFit(label.winfo_reqwidth())

if isinstance(scentKey,str):
    scentKey = keyboard.KeyCode(char=scentKey)

root.geometry(wingeo)

if setKey == 0:
    label.config(text='{:,}'.format(count))
    labeltip.setText(f'群怪数量： {quantity}\n甜甜香气按键： {scentKey}')
    resizeToFit()

def save():
    if setKey == 0:
        file = open('encounters.py', 'w')
        try:
            file.write(f'#!/bin/python3\nfrom pynput import keyboard\nquantity = {quantity}\ncount = {count}\nscentKey = \'{scentKey.char}\'\nwingeo = "+{root.winfo_x()}+{root.winfo_y()}"')
        except AttributeError:
            file.write(f'#!/bin/python3\nfrom pynput import keyboard\nquantity = {quantity}\ncount = {count}\nscentKey = keyboard.{scentKey}\nwingeo = "+{root.winfo_x()}+{root.winfo_y()}"')
        file.close()
        if not pause:
            label.config(text='{:,}'.format(count))
            labeltip.setText(f'群怪数量： {quantity}\n甜甜香气按键： {scentKey}')
        root.update()

def inc(n):
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

def dec(n):
    global count, last, undoPoint, undoButton
    count -= n
    undoPoint += 1
    if undoPoint > 49:
        last.pop(0)
        last.append(n*-1)
        undoPoint = 49
    else:
        last[undoPoint] = n
    if undoButton["state"] == "disabled":
        undoButton["state"] = "normal"
    save()

def on_press(key):
    global modifier, scentKey, setKey, altMod, shiftMod, superMod, undoButton
    if pause == False and modifier == True and altMod == False and shiftMod == False and superMod == False:
        if key == keyboard.KeyCode(char='+') or key == keyboard.KeyCode(char='='):
            inc(1)
        elif key == keyboard.KeyCode(char='*') or key == keyboard.KeyCode(char='8'):
            inc(quantity)
        elif key == keyboard.KeyCode(char='-'):
            dec(1)
        elif key == keyboard.KeyCode(char='/'):
            dec(quantity)
        elif key == keyboard.KeyCode(char='z'):
            if undoPoint == 0 and last[undoPoint] == 0:
                undoButton["state"] = "disabled"
            else:
                undo()
        elif key == keyboard.Key.esc:
            configure()
        elif key == keyboard.KeyCode(char='h'):
            setKey = 1
            configure()
    elif modifier == False and altMod == True and shiftMod == False and superMod == False:
        if key == keyboard.Key.esc:
            togglePause()
    if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        modifier = True
    elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr:
        altMod = True
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
        shiftMod = True
    elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
        superMod = True

def on_release(key):
    global modifier, scentKey, setKey, quantity, altMod, shiftMod, superMod
    if pause == False and modifier == False and altMod == False and shiftMod == False and superMod == False:
        if setKey == 1:
            scentKey = key
            configure()
        elif setKey == 2:
            try:
                keyChar = key.char
            except AttributeError:
                keyChar = 'n'
            if keyChar.isdigit() and int(keyChar) > 0:
                quantity = int(keyChar)
                label.config(text='{:,}'.format(count))
                labeltip.setText(f'群怪数量：  {quantity}\n甜甜香气按键： {scentKey}')
                resizeToFit()
                root.update()
                setKey = 0
            else:
                configure(True)
        elif key == scentKey:
            inc(quantity)
    if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        modifier = False
    elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r or key == keyboard.Key.alt_gr:
        altMod = False
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
        shiftMod = False
    elif key == keyboard.Key.cmd or key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
        superMod = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    root.mainloop()
    listener.join()
