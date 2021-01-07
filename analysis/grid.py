# Final version
import argparse
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
		f = open('coords.txt','a+')
		f.write(str(event.y)+','+str(event.x)+'\n')
		f.close()
		if (len(pos_points) == 2):
			root.destroy()
		
	#mouseclick event
	canvas.bind("<ButtonPress-1>",printcoords)

	root.mainloop()


	
	return pos_points

def load(path,output_path,pos_points):
	# Load the image
	img = plt.imread(path)

	img_name = path.split('/')[-1]
	img_name = img_name.split('.',1)[0]

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
	### 1st value defines the vertical range, second value defines the horizontal range

	img[top_left[0]:bot_right[0] ,top_left[1]:bot_right[1]:dy,:] = grid_color # Vertical lines
	img[top_left[0]:bot_right[0]:dx,top_left[1]:bot_right[1],:] = grid_color # Horizontal lines

	# Store the result
	plt.axis('off')
	plt.grid(b=None)
	plt.imshow(img)
	plt.savefig(output_path + '/' + img_name + '_grid.png' ,bbox_inches='tight')
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='grid sketch')
	parser.add_argument('--image', type=str, default='img/goalkeeper.png')
	parser.add_argument('--output', type=str, default='output')

	args = parser.parse_args()

	try:
		with open('coords.txt') as f:
			pos_points = [tuple(map(int, i.split(','))) for i in f]
	except IOError:
		pos_points = grid(args.image)

	load(args.image,args.output,pos_points)
