#GUI that reads in a file and determines what type of transforms can be done on it

import string
import sys
import numpy as np
import tkinter as tk
import math
from TransformState import State

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog	# used to be named tkFileDialog		
import cv2
import imghdr
import os.path

matchType = 0


def select_file():
	# grab a reference to the image panel
	global panelA
	global extension

	# open a file chooser dialog and allow the user to select a file
	path = filedialog.askopenfilename()
	print("Name of the file is: ", path)

	# ensure a file path was selected
	if len(path) > 0:
		# load the image from disk and convert it to grayscale
		image = cv2.imread(path)


		extension = os.path.splitext(path)[1]
		print("Extension is: ", extension)

		#TODO - Determine if file extension is valid
		if(extension == '.jpg'):
			print("MATCHED")
			matchType = 1

		if(extension == '.bmp'):
			print("MATCHED")

		# Convert image so that it's usable in tkinter
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = Image.fromarray(image)
		image = image.resize((250, 250), Image.ANTIALIAS)	#Resize image
		image = ImageTk.PhotoImage(image)

		# if the panels are None, initialize them
		if panelA is None:
			# the8g will store our original image
			panelA = Label(image=image)
			panelA.image = image
			#panelA.pack(side="left", padx=10, pady=10)
			panelA.place(relx=.28, rely=.27, anchor='n')
		# otherwise, update the image panels
		else:
			panelA.configure(image=image)
			panelA.image = image

	# Make buttons asking for compression types
	if(extension == '.jpg'):
		btnJPEG = Button(root, height=2, width=30, text="JPEG Compression", command=transform_selected)
		btnJPEG.place(relx=.25, rely=0.69, anchor='n')

		btnLZW = Button(root, height=2, width=30, text="LZW Compression", command=transform_selected)
		btnLZW.place(relx=.25, rely=0.75, anchor='n')

		btnRLE = Button(root, height=2, width=30, text="Run Length Encoding", command=transform_selected)
		btnRLE.place(relx=.25, rely=0.81, anchor='n')

		btnARI = Button(root, height=2, width=30, text="Arithmetic Encoding", command=transform_selected)
		btnARI.place(relx=.25, rely=0.87, anchor='n')

		btnHUFF = Button(root, height=2, width=30, text="Huffman Encoding", command=transform_selected)
		btnHUFF.place(relx=.25, rely=0.93, anchor='n')

		btnSUB = Button(root, height=2, width=30, text="Subsampling", command=transform_selected)
		btnSUB.place(relx=.75, rely=0.69, anchor='n')

		btnQUANT = Button(root, height=2, width=30, text="Quantization", command=transform_selected)
		btnQUANT.place(relx=.75, rely=0.75, anchor='n')

		btnDIT = Button(root, height=2, width=30, text="Dithering", command=transform_selected)
		btnDIT.place(relx=.75, rely=0.81, anchor='n')

		btnCOL = Button(root, height=2, width=30, text="Color Space Changer", command=transform_selected)
		btnCOL.place(relx=.75, rely=0.87, anchor='n')

		btnRES = Button(root, height=2, width=30, text="Restart", command=restart)
		btnRES.place(relx=.75, rely=0.93, anchor='n')




# Function for handling when a button is pressed
def transform_selected():
	x = 0


# Function for handling when restart is pressed
def restart():
	x = 0





# initialize the window toolkit along with the image panel
root = Tk()
root.geometry("500x700+10+80")
panelA = None

# btn1 - Ask for file input
btn1 = Button(root, height=10, width=50, text="Select a file", command=select_file)
btn1.pack(side="top", padx="10", pady="10")

# T1 - Displays image information
T1 = tk.Text(root, height=15, width=25)
T1.pack(side="right", padx="10", pady="10")
T1.insert(tk.END, "    Image information")
T1.place(relx=.77, rely=0.275, anchor='n')


# T2 - Display 'Available Transformations'
T2 = tk.Text(root, height=1, width=59)
T2. pack(side="left", padx="10", pady="10")
T2.insert(tk.END, "                Available Transformations:     ")
T2.place(relx=.50, rely=0.65, anchor='n')


#TO DO place available transforms


#TO DO Determine which transforms are available

# kick off the GUI
root.mainloop()