import tkinter as tk
from functools import partial
import functions
import display_app

defense_folder = "./record/goal/"
attack_folder = "./record/attack_seq/"
analysis_folder = "./analysis/"

wh = 600
ww = 900

win = tk.Tk()

dis_app = display_app.Display_App(win, defense_folder, attack_folder, analysis_folder, wh, ww)

dis_app.run()