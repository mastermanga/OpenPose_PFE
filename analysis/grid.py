# Final version
import sys
from tkinter import *
import pylab as plt

def grid(path):

	root = Tk()

	#setting up a tkinter canvas with scrollbars
	frame = Frame(root, bd=2, relief=SUNKEN)
	frame.grid_rowconfigure(0, weight=1)
	frame.grid_columnconfigure(0, weight=1)
	xscroll = Scrollbar(frame, orient=HORIZONTAL)
	xscroll.grid(row=1, column=0, sticky=E+W)
	yscroll = Scrollbar(frame)
	yscroll.grid(row=0, column=1, sticky=N+S)
	canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
	canvas.grid(row=0, column=0, sticky=N+S+E+W)
	xscroll.config(command=canvas.xview)
	yscroll.config(command=canvas.yview)
	frame.pack(fill=BOTH,expand=1)

	#adding the image
	img_tk = PhotoImage(file=path)
	canvas.create_image(0,0,image=img_tk,anchor="nw")
	canvas.config(scrollregion=canvas.bbox(ALL))

	global pos_points
	
	pos_points = []

	#function to be called when mouse is clicked
	def printcoords(event):
		#outputting x and y coords to console
		pos_points.append((int(event.y),int(event.x)))
		if (len(pos_points) == 2):
			root.destroy()
	#mouseclick event
	canvas.bind("<ButtonPress-1>",printcoords)

	root.mainloop()
	
	return pos_points

def load(path,pos_points,output_path):
	# Load the image
	img = plt.imread(path)

	# Designate points
	top_left = pos_points[0]
	bot_right = pos_points[1]

	# Grid lines at these intervals (in pixels)
	# dx and dy can be different
	# dx, dy = 100,100
	dx = int((bot_right[0] - top_left[0])/5)
	dy = int((bot_right[1] - top_left[1])/5)

	print("Top left coordinates :",top_left)
	print("Bottom right coordinates:",bot_right)
	print("Computed intervals :",dx,dy)
	# Custom (rgb) grid color
	grid_color = [0,0,0]

	# Modify the image to include the grid
	img[top_left[0]:bot_right[0] ,top_left[1]::dy,:] = grid_color
	img[top_left[0]::dx,top_left[1]:bot_right[1],:] = grid_color

	# Store the result
	plt.axis('off')
	plt.grid(b=None)
	plt.imshow(img)
	plt.savefig(sys.argv[2],bbox_inches='tight')
	
if __name__ == '__main__':
	try:
		with open('coords.txt') as f:
			pos_points = [tuple(map(int, i.split(','))) for i in f]
	except IOError:
		pos_points = grid(sys.argv[1])
	
	load(sys.argv[1],pos_points,sys.argv[2])
