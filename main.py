from infi.systray import SysTrayIcon
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from functools import partial
import sys
import win32ui
import win32gui
import win32con
import win32api
import PIL
from PIL import Image
from pathlib import Path


author = "Handy Tray © Ingemars 2018"
NORM_FONT = ("Verdana", 10)
hover_text = "Handy Tray"
fileDir = os.path.dirname(os.path.realpath('__file__'))

def deleteApps():
    osCommandString = "Notepad2.exe config.ini"
    os.system(osCommandString)
    print(osCommandString)


def iconextract(path, filename):
    try:
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
        large, small = win32gui.ExtractIconEx(path, 0)
        win32gui.DestroyIcon(large[0])
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), small[0])
        hbmp.SaveBitmapFile(hdc, filename + ".bmp")
        img = Image.open(filename + ".bmp")
        img.save(filename + '.ico')
        for p in Path(".").glob("*.bmp"):
            p.unlink()
    except:
        pass


def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def popupmsg(msg):
    popup = tk.Tk()
    popup.iconbitmap('tray.ico')
    popup.resizable(0, 0)
    w = 500
    h = 180
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    popup.overrideredirect(0)
    popup.wm_title(hover_text + ' - Add/Delete Software')
    label = ttk.Label(popup, text="Program Path:", font=NORM_FONT)
    label2 = ttk.Label(popup, text="Description:", font=NORM_FONT)
    label3 = ttk.Label(popup, text="(Optional)", font=NORM_FONT)
    label_credits = ttk.Label(popup, text=author, font=NORM_FONT)
    program = tk.Entry(popup, width=50)

    def browse_program():
        file = fd.askopenfile(initialdir="/", title="Select file", filetypes=(("exe files", "*.exe"), ("all files", "*.*")))
        if file:
            program.insert(0, file.name)


    Button_Program_Select = ttk.Button(popup, text="Browse", command=browse_program)
    label.grid(row=0, column=0, ipady=20, ipadx=2, padx=2, sticky='w')
    program.grid(row=0, column=1)
    Button_Program_Select.grid(row=0, column=2, padx=2)
    label2.grid(row=1, column=0, ipady=0, ipadx=2, padx=2, sticky='w')
    label3.grid(row=1, column=2, padx=0)
    description = tk.Entry(popup, width=50)
    description.grid(row=1, column=1)

    def save():
        if len(program.get()) > 0:
            f = open("config.ini", "a")
            f.write((program.get() + ' ## ' + description.get() + '\n'))
            f.close()
            popup.destroy()
            restart_program()
        else:
            popup.destroy()
            restart_program()


    Button_Save = ttk.Button(popup, text="Save", command=save)
    Button_Save.grid(row=3, column=1, pady=10, padx=10)
    Button_Cancel = ttk.Button(popup, text="Cancel", command=popup.destroy)
    Button_Cancel.grid(row=4, column=2)
    Button_Delete = ttk.Button(popup, text="Remove/Edit Apps", command=deleteApps)
    Button_Delete.grid(row=4, column=1)
    label_credits.grid(row=5, column=0, ipady=10, columnspan=3)
    popup.mainloop()


menu_options = ()
softlist = []


def callback_function(self, path):
    print(path)
    os.startfile(path)


try:
    with open("config.ini", "r") as config:
        for line in config:
            line = ''.join(line)
            start_dsc = line.find('##')
            start_file = line.rfind('/')
            filename = line[start_file + 1: start_dsc].replace(" ", "")
            path = line[:start_dsc - 1]
            description = line[start_dsc + 3:]
            new_callback_function = partial(callback_function, path=path)
            callback = new_callback_function
            iconextract(path, filename)
            if len(description) > 1:
                sep = ' || '
            else:
                sep = ' '
            softlist.append((filename + sep + description, filename + ".ico", callback))
except:
    pass


softlist.append(('Add/Del Software', 'add.ico', popupmsg))
for i in range(0, len(softlist)):
    menu_options += (softlist[i],)

sysTrayIcon = SysTrayIcon('tray.ico', hover_text, menu_options, default_menu_index=len(softlist)-1)
sysTrayIcon.start()