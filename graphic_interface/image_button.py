import tkinter as tk
from PIL import Image, ImageTk
import functions

class image_button():
	def __init__(self, window, photo_path):
		self.frame = tk.Frame(window, highlightbackground="black", highlightthickness=1, cursor="hand1")
		# window.winfo_height()
		# window.winfo_width()
		self.frame.pack(expand=True, fill="both")
		# self.frame.grid(padx=10, pady=10)

		self.frame.bind('<Configure>', self.on_resize)
		# self.frame.bind('<Button-1>', self.e)

		self.photo_path = photo_path
		self.org_image = Image.open(photo_path)
		self.image = self.org_image
		self.image = self.image.resize((int(self.image.size[0]/1.5), int(self.image.size[1]/1.5)))
		self.photo = ImageTk.PhotoImage(self.image)

		# self.canvas = tk.Canvas(self.frame, width = self.image.size[0], height = self.image.size[1]) 
		# self.canvas.create_image(0,0, anchor = tk.NW, image=self.photo)
		# self.canvas.pack() 

		self.label = tk.Label(self.frame, image=self.photo)
		self.label.image = self.photo
		self.label.pack(expand=True, fill="both", side="top")
		self.label.bind('<Button-1>', self.on_click)

		self.label_2 = tk.Label(self.frame, text="TEXT", height=5)
		self.label_2.pack(fill='x', side="bottom")
		self.label_2.bind('<Button-1>', self.on_click)

	def on_resize(self, event):
		print("Event", event.width, event.height)
		print("Frame :", self.frame.winfo_width(), self.frame.winfo_height())
		print("Image :", self.image.size[0], self.image.size[1])
		self.image = self.org_image.resize((event.width-4, event.height-63))
		self.photo = ImageTk.PhotoImage(self.image)

		self.label.configure(image=self.photo)
		self.label.image = self.photo

	def on_click(self, event):
		functions.open_video(self.photo_path)
		print("click")


class img_btn(tk.Frame):
	def __init__(self, window, image, text, video_path):
		super(img_btn, self).__init__(window, highlightbackground="black", highlightthickness=1, cursor="hand1")
		self.pack(expand=True, fill="both")

		self.bind('<Configure>', self.on_resize)
		# self.bind('<Button-1>', self.on_click)

		self.video_path = video_path

		self.org_image = image
		self.image = self.org_image
		self.image = self.image.resize((int(self.image.size[0]/1.5), int(self.image.size[1]/1.5)))
		self.photo = ImageTk.PhotoImage(self.image)

		self.label = tk.Label(self, image=self.photo)
		self.label.image = self.photo
		self.label.pack(expand=True, fill="both", side="top")
		self.label.bind('<Button-1>', self.on_click)
		
		# self.label.place(relwidth=1.0, relheight=0.9)

		self.label_2 = tk.Label(self, text=text, height=3)
		self.label_2.pack(fill='x', side="bottom")
		self.label_2.bind('<Button-1>', self.on_click)
		
		# self.label_2.place(anchor='s', relwidth=1.0, relheight=0.1)

	def on_resize(self, event):
		self.image = self.org_image.resize((event.width, event.height-30))
		self.photo = ImageTk.PhotoImage(self.image)

		self.label.configure(image=self.photo)
		self.label.image = self.photo

	def on_click(self, event):
		functions.open_video(self.video_path)
