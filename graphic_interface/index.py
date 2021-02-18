# coding: utf-8
from functools import partial
from tkinter import *

# Import header.py and functions.py
import header
import functions
import display_app

def open_records(window):
    # window.withdraw()
    defense_folder = "./record/goal/"
    attack_folder = "./record/attack_seq/"
    analysis_folder = "./analysis/"

    wh = 600
    ww = 900

    dis_app = display_app.Display_App(window, defense_folder, attack_folder, analysis_folder, wh, ww)

    dis_app.run()

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
btnAnalyse = Button(window, text='Voir analyses', command=partial(open_records, window))

frameCnt = 36
frames = [PhotoImage(file="graphic_interface/" + 'hocket.gif', format='gif -index %i' % i) for i in range(frameCnt)]


# Deploy "window"
lfBienvenue.pack(fill="both", expand="yes", padx=10, pady=5)

label = Label(lfBienvenue)

label.pack(side=TOP)
btnLancer.pack(side=LEFT, padx=80, pady=5)
btnQuitter.pack(side=RIGHT, padx=80, pady=5)
btnAnalyse.pack(padx=80, pady=5)

window.after(0, update, 0)
window.mainloop()
