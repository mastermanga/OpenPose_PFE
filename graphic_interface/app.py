import os
from functools import partial
from tkinter import *


class App():
    def __init__(self, defense_folder, attack_folder, analysis_folder, wh, ww):
        self.window = Tk()
        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.lf_bienvenue = LabelFrame(self.window, text=" Bienvenue ", padx=10, pady=10)
        self.label = Label(self.lf_bienvenue)
        self.spinbox = Spinbox(box, from_=1, to=10, width=2)

        self.defense_folder = defense_folder
        self.attack_folder = attack_folder
        self.analysis_folder = analysis_folder
        self.wh, self.ww = wh, ww

        self.create_window(wh, ww)
        self.create_nav_menu()

    def create_window(self, wh, ww):
        self.window.title("Simulateur : Gardien de hocket sur gazon")

        self.window.geometry("{}x{}".format(ww, wh))
        self.window.minsize(int(ww / 2), int(wh / 2))
        self.window.maxsize(int(ww * 2), int(wh * 2))

    def create_nav_menu(self):

        #TODO
        self.menu.add_command(label="Voir les vidéos et analyses", command='#TODO')
        self.menu.add_command(label="Lancer une simulation", command=self.avant_simulation)
        self.menubar.add_cascade(label="Naviguer", menu=self.menu)

    def create_main_frame(self):
        self.lf_bienvenue.pack(fill="both", expand="yes", padx=10, pady=5)

    def avant_simulation(self):
        self.window.withdraw()
        box = Toplevel(master=self.window)
        box.title("Lancer une simulation")
        box.geometry("325x90")
        box.protocol('WM_DELETE_WINDOW', partial(self.on_closing, box, self.window))
        self.label = Label(box, text="Combien d'attaques voulez-vous lancer ?")
        btn = Button(box, text="Lancer", command=partial(lancer_simulation, spinbox, box))

        label.pack(side=TOP)
        spinbox.pack()
        btn.pack(side=BOTTOM, padx=80, pady=5)

    def lancer_simulation(spinbox, box):
        try:
            nb_run = str(spinbox.get())
            box.destroy()
            os.system('python ../record/record.py --runs ' + nb_run)
        except IndexError:
            print("No file selected")

    def on_closing(box, window):
        window.deiconify()
        box.destroy()

    def update(self, ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        self.label.configure(image=frame)
        self.window.after(100, update, ind)

    def run(self):
        self.window.mainloop()
