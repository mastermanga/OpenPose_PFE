# coding: utf-8
from functools import partial
from tkinter import *

# Import header.py and functions.py
import header
import functions


# Functions
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    window.after(100, update, ind)


# Build "window"
window = header.header()

lfBienvenue = LabelFrame(window, text=" Bienvenue ", padx=10, pady=10)

#TODO
btnLancer = Button(window, text='Lancer', command=partial(functions.avant_simulation, window))
btnQuitter = Button(window, text='Quitter', command=window.quit)

frameCnt = 36
frames = [PhotoImage(file="graphic_interface/" + 'hocket.gif', format='gif -index %i' % i) for i in range(frameCnt)]


# Deploy "window"
lfBienvenue.pack(fill="both", expand="yes", padx=10, pady=5)

label = Label(lfBienvenue)

label.pack(side=TOP)
btnLancer.pack(side=LEFT, padx=80, pady=5)
btnQuitter.pack(side=RIGHT, padx=80, pady=5)

window.after(0, update, 0)
window.mainloop()
