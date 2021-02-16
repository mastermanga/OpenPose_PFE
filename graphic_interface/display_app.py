import os, sys
from functools import partial
import tkinter as tk
from PIL import Image, ImageTk
import functions

class Display_App():
    def __init__(self, defense_folder, attack_folder, analysis_folder, wh, ww):
        self.defense_folder = defense_folder
        self.attack_folder = attack_folder
        self.analysis_folder = analysis_folder
#         self.wh, self.ww = wh, ww
        
        self.create_window(wh, ww)
        self.create_main_frame()
        self.create_rec_button()
        self.create_menus()
        self.create_display_frame()
            
    def parse_video_name(self, name):
        date, time, attack_video = name.split('_')
        attack_video = '.'.join(attack_video.split('.')[:2])
        
        return date, time, attack_video
    
    def set_current_video(self):
        video_dt = self.date_var.get() + '_' + self.time_var.get()
        
        for v in os.listdir(self.defense_folder + self.date_var.get() + '/'):
            if v.startswith(video_dt):
                self.current_video = v
                break
                
    def get_defense(self):
        return self.defense_folder + self.date_var.get() + '/' + self.current_video
    
    def get_attack(self):
        attack = self.parse_video_name(self.current_video)[2]
            
        return self.attack_folder + attack
        
    def get_analysis(self):
        date = self.parse_video_name(self.current_video)[0]
        defense = self.current_video
        
        for analysis in os.listdir(self.analysis_folder + date + '/'):
            if analysis == defense:
                return self.analysis_folder + date + '/' + analysis
        
        return None
    
    def launch_analysis(self):
        f = open(self.analysis_folder + self.parse_video_name(self.current_video)[0] + '/' + self.current_video, "x")
        self.update_display_frame(None)
        
    def create_window(self, wh, ww):
        self.window = tk.Tk()
        self.window.geometry("{}x{}".format(ww, wh))
        self.window.minsize(int(ww/2), int(wh/2))
        self.window.maxsize(int(ww*2), int(wh*2))

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(expand=True, fill="both")

        for i in range(12):
            self.main_frame.rowconfigure(i, weight=1, uniform="frame_rows")
        for j in range(12):
            self.main_frame.columnconfigure(j, weight=1, uniform="frame_cols")
        
    def create_rec_button(self):
        self.frame_1 = tk.Frame(self.main_frame, bd=4, relief="ridge", bg="white")
        self.frame_1.grid(column=0, row=0, columnspan=3, sticky="nesw")
        
        self.btn = tk.Button(self.frame_1, text="go to recording", bd=1, relief="raised")
        self.btn.place(relheight=1.0, relwidth=1.0)
        
    def create_menus(self):
        self.frame_2 = tk.Frame(self.main_frame, bd=4, relief="ridge", bg="pink")
        self.frame_2.grid(column=0, row=1, columnspan=3, rowspan=11, sticky="nesw")
        
        date_list = os.listdir(self.defense_folder)
        date_list.sort(reverse=True)

        self.date_var = tk.StringVar()
        self.date_var.set(date_list[0])

        self.date_menu = tk.OptionMenu(self.frame_2, self.date_var, *date_list, command=self.update_time_menu)
        self.date_menu.place(relheight=0.07, relwidth=0.7, relx=0.15, rely=0.2)
        
        self.time_var = tk.StringVar()

        self.time_menu = tk.OptionMenu(self.frame_2, self.time_var, None)
        self.time_menu.place(relheight=0.07, relwidth=0.7, relx=0.15, rely=0.55)
        
        self.update_time_menu(None)

    def update_time_menu(self, date):
        time_list = []
        for v in os.listdir(self.defense_folder + self.date_var.get() + '/'):
            time_list.append(self.parse_video_name(v)[1])
        time_list.sort(reverse=True)
        
        self.time_var.set(time_list[0])
        
        menu = self.time_menu.children["menu"]
        menu.delete(0, "end")
        
        for t in time_list:
            menu.add_command(label=t, command=partial(self.menu_command, t))
            
        self.update_display_frame(None)
            
    def menu_command(self, time):
        self.time_var.set(time)
        self.update_display_frame(time)

    def create_display_frame(self):
        self.frame_3 = tk.Frame(self.main_frame, bd=4, relief="ridge", bg="pink")
        self.frame_3.grid(column=3, row=0, columnspan=9, rowspan=12, sticky="nesw")
        
        if self.get_analysis():
            self.raw_defense = tk.Button(self.frame_3, text=self.get_defense(), bd=2, relief="raised")
            self.raw_defense.place(relheight=0.4, relwidth=0.45, relx=0.3, rely=0.05)

            self.attack = tk.Button(self.frame_3, text=self.get_attack(), bd=2, relief="raised")
            self.attack.place(relheight=0.4, relwidth=0.45, relx=0.025, rely=0.55)

            self.analysis = tk.Button(self.frame_3, text=self.get_analysis(), bd=2, relief="raised")
            self.analysis.place(relheight=0.4, relwidth=0.45, relx=0.525, rely=0.55)
        else:
            self.raw_defense = tk.Button(self.frame_3, text=self.get_defense(), bd=2, relief="raised")
            self.raw_defense.place(relheight=0.35, relwidth=0.45, relx=0.3, rely=0.05)

            self.attack = tk.Button(self.frame_3, text=self.get_attack(), bd=2, relief="raised")
            self.attack.place(relheight=0.35, relwidth=0.45, relx=0.3, rely=0.5)

            self.analysis = tk.Button(self.frame_3, text="launch analysis", bd=2, relief="raised", command=self.launch_analysis)
            self.analysis.place(relheight=0.08, relwidth=1.0, rely=0.92)

    def update_display_frame(self, time):
        self.set_current_video()
        # destroy frame if exists
        try:
            self.frame_3.destroy()
        except AttributeError:
            pass
        # create new frame and add it to main_frame
        self.create_display_frame()
     
    
    def run(self):
        self.window.mainloop()