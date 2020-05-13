#GUI that reads in a file and determines what type of transforms can be done on it

import tkinter as tk
from GUI.Common import *
import ARI
import DIT
import Huffman
import JPEG
import LZW
import RLE


matchType = 0

class WidgetInformation:
	def __init__(self, name, inType, outType):
		self.name = name
		self.inType = inType
		self.outType = outType


class TransformResolver(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.pack()
		T2 = tk.Label(self, height=1, width=59, text = "Avaliable Transformations")
		T2.pack(side="top")#place(side="left", padx="10", pady="10")
		self.selected_label = tk.Label(self, heigh = 1, width = 59, text = "Selected: ")
		self.selected_label.pack(side = "top")
		self.init_widgets()
		self.selected = None
		# T2.insert(tk.END, "                Available Transformations:     ")
		# T2.place(relx=.50, rely=0.65, anchor='n')
	def init_widgets(self):
		self.btnJPEG = tk.Button(self, height=2, width=30, text="JPEG Compression", command=self.transform_selected(WidgetInformation("JPEG Compression", TYPE_BITMAP, TYPE_ENCODED), lambda: JPEG.Jpeg().encode))
		#self.btnJPEG.pack(side = "left")#(relx=.25, rely=0.69, anchor='n')

		self.btnLZW = tk.Button(self, height=2, width=30, text="LZW Compression", command=self.transform_selected(WidgetInformation("LZW Compression", TYPE_BYTES, TYPE_BYTES), lambda: LZW.LZW().encode))
		#self.btnLZW.pack(side = "left")#place(relx=.25, rely=0.75, anchor='n')

		self.btnRLE = tk.Button(self, height=2, width=30, text="Run Length Encoding", command=self.transform_selected(WidgetInformation("RLE Compression", TYPE_BYTES, TYPE_BYTES), lambda: RLE.RLE(2).encode))
		#self.btnRLE.pack(side = "left")#place(relx=.25, rely=0.81, anchor='n')

		self.btnARI = tk.Button(self, height=2, width=30, text="Arithmetic Encoding", command=self.transform_selected(WidgetInformation("ARI Compression", TYPE_BYTES, TYPE_BYTES), lambda : ARI.ARI(1).encode))
		#self.btnARI.pack(side = "left")#place(relx=.25, rely=0.87, anchor='n')

		#TODO: Make huffman standard to transformation format
		self.btnHUFF = tk.Button(self, height=2, width=30, text="Huffman Encoding", command=self.transform_selected(WidgetInformation("Huffman Compression", TYPE_BYTES, TYPE_BYTES), lambda : Huffman.Huffman().encode))
		#self.btnHUFF.pack(side = "left")#place(relx=.25, rely=0.93, anchor='n')

	def select_transform(self, inType, outType):
		# grab a reference to the image panel
		# global panelA
		# global extension

		# # open a file chooser dialog and allow the user to select a file
		# path = filedialog.askopenfilename()
		# print("Name of the file is: ", path)
		#
		# # ensure a file path was selected
		# if len(path) > 0:
		# 	# load the image from disk and convert it to grayscale
		# 	image = cv2.imread(path)
		#
		#
		# 	self.extension = os.path.splitext(path)[1]
		# 	print("Extension is: ", self.extension)
		#
		# 	#TODO - Determine if file extension is valid
		# 	if(self.extension == '.jpg'):
		# 		print("MATCHED")
		# 		matchType = 1
		#
		# 	if(self.extension == '.bmp'):
		# 		print("MATCHED")
		#
		# 	# Convert image so that it's usable in tkinter
		# 	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# 	image = Image.fromarray(image)
		# 	image = image.resize((250, 250), Image.ANTIALIAS)	#Resize image
		# 	image = ImageTk.PhotoImage(image)

		# if the panels are None, initialize them
		# if self.panelA is None:
		# 	# the8g will store our original image
		# 	panelA = Label(image=image)
		# 	panelA.image = image
		# 	#panelA.pack(side="left", padx=10, pady=10)
		# 	panelA.place(relx=.28, rely=.27, anchor='n')
		# # otherwise, update the image panels
		# else:
		# 	self.panelA.configure(image=image)
		# 	self.panelA.image = image
		self.btnJPEG.pack_forget()

		self.btnLZW.pack_forget()

		#self.btnLZW.pack(side = "left")#place(relx=.25, rely=0.75, anchor='n')

		self.btnRLE.pack_forget()
		self.btnARI.pack_forget()
		self.btnHUFF.pack_forget()
		# Make buttons asking for compression types
		if (inType == TYPE_BITMAP or inType == None) or (outType == TYPE_ENCODED or outType == None):
			#TODO: Make JPEG standard to transformation format
			self.btnJPEG.pack(side = "left")#(relx=.25, rely=0.69, anchor='n')
		if (inType == TYPE_BYTES or inType == None) or (outType == TYPE_BYTES or outType == None):
			self.btnLZW.pack(side = "left")#place(relx=.25, rely=0.75, anchor='n')

			self.btnRLE.pack(side = "left")#place(relx=.25, rely=0.81, anchor='n')

			self.btnARI.pack(side = "left")#place(relx=.25, rely=0.87, anchor='n')

			self.btnHUFF.pack(side = "left")#place(relx=.25, rely=0.93, anchor='n')
		if (inType == TYPE_BITMAP or inType == None) or (outType == TYPE_BITMAP or outType == None):
			pass
			#TODO: make buttons

			# btnSUB = Button(self, height=2, width=30, text="Subsampling", command=transform_selected(WidgetInformation("Subsampling", "")))
			# btnSUB.place(relx=.75, rely=0.69, anchor='n')
			#
			# btnQUANT = Button(self, height=2, width=30, text="Quantization", command=transform_selected)
			# btnQUANT.place(relx=.75, rely=0.75, anchor='n')
			#
			# btnDIT = Button(self, height=2, width=30, text="Dithering", command=transform_selected)
			# btnDIT.place(relx=.75, rely=0.81, anchor='n')
			#
			# btnCOL = Button(self, height=2, width=30, text="Color Space Changer", command=transform_selected)
			# btnCOL.place(relx=.75, rely=0.87, anchor='n')

			# btnRES = Button(self, height=2, width=30, text="Restart", command=restart)
			# btnRES.place(relx=.75, rely=0.93, anchor='n')




	# Function for handling when a button is pressed
	def transform_selected(self, widgetInformation, transformGetter):
		def handler():
			self.selected_label['text'] = "Selected: " + widgetInformation.name
			self.selected = widgetInformation
			self.selected.function = transformGetter()
		return handler



	# # Function for handling when restart is pressed
	# def restart():
	# 	x = 0





	# # initialize the window toolkit along with the image panel
	# root = Tk()
	# root.geometry("500x700+10+80")
	# panelA = None
	#
	# # btn1 - Ask for file input
	# btn1 = Button(root, height=10, width=50, text="Select a file", command=select_file)
	# btn1.pack(side="top", padx="10", pady="10")
	#
	# # T1 - Displays image information
	# T1 = tk.Text(root, height=15, width=25)
	# T1.pack(side="right", padx="10", pady="10")
	# T1.insert(tk.END, "    Image information")
	# T1.place(relx=.77, rely=0.275, anchor='n')
	#

	# T2 - Display 'Available Transformations'


	#TO DO place available transforms


	#TO DO Determine which transforms are available

# kick off the GUI
#root.mainloop()