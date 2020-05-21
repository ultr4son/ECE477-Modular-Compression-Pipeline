#GUI that reads in a file and determines what type of transforms can be done on it

import tkinter as tk
import Constants
import GUI.ParameterInput as ParameterInput
from GUI.Common import *
import ARI
import DIT
import Huffman
import JPEG
import LZW
import RLE
import color_quantization
import color_space
import inspect

matchType = 0



class WidgetInformation:

	def __init__(self, name, inType, outType, transformInitializer):
		self.name = name
		self.inType = inType
		self.outType = outType
		self.transformInitializer = transformInitializer
def get_default_args(func):
	signature = inspect.signature(func)
	return {
		k: v.default
		for k, v in signature.parameters.items()
		if v.default is not inspect.Parameter.empty
	}
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
		self.btnJPEG = tk.Button(self, height=2, width=30, text=Constants.JPEG_ENCODING,
								 command=self.transform_selected(WidgetInformation(Constants.JPEG_ENCODING, TYPE_BITMAP, TYPE_ENCODED, lambda **kwargs: JPEG.Jpeg(kwargs).encode)))
		self.btnDIT = tk.Button(self, height = 2, width=30, text=Constants.DITHERING, command=self.transform_selected(WidgetInformation(Constants.DITHERING, TYPE_BITMAP, TYPE_BITMAP, lambda **kwargs: DIT.Dither(kwargs).encode)))
		self.btnRGB = tk.Button(self, height = 2, width=30, text=Constants.RGB, command=self.transform_selected(WidgetInformation(Constants.RGB, TYPE_BITMAP, TYPE_BITMAP, lambda **kwargs: color_space.Color_Space(kwargs).RGB)))
		self.btnYUV = tk.Button(self, height = 2, width=30, text=Constants.YUV, command=self.transform_selected(WidgetInformation(Constants.YUV, TYPE_BITMAP, TYPE_BITMAP, lambda **kwargs: color_space.Color_Space(kwargs).YUV)))
		self.btnGreyscale = tk.Button(self, height = 2, width=30, text=Constants.GREYSCALE, command=self.transform_selected(WidgetInformation(Constants.GREYSCALE, TYPE_BITMAP, TYPE_BITMAP, lambda **kwargs: color_space.Color_Space(kwargs).Gray)))
		self.btnColorQuantization = tk.Button(self, height = 2, width=30, text=Constants.COLOR_QUANTIZATION, command=self.transform_selected(WidgetInformation(Constants.COLOR_QUANTIZATION, TYPE_BITMAP, TYPE_BITMAP, lambda **kwargs: color_quantization.Color_Quantizaion(kwargs).kmeans_quantization)))

		self.btnLZW = tk.Button(self, height=2, width=30, text=Constants.LZW_ENCODING, command=self.transform_selected(WidgetInformation("LZW Compression", TYPE_BYTES, TYPE_BYTES, lambda **kwargs: LZW.LZW(kwargs).encode)))
		self.btnRLE = tk.Button(self, height=2, width=30, text=Constants.RUN_LENGTH_ENCODING, command=self.transform_selected(WidgetInformation("RLE Compression", TYPE_BYTES, TYPE_BYTES, lambda **kwargs: RLE.RLE(kwargs).encode)))
		self.btnARI = tk.Button(self, height=2, width=30, text=Constants.ARITHMETIC_CODING, command=self.transform_selected(WidgetInformation("ARI Compression", TYPE_BYTES, TYPE_BYTES, lambda **kwargs: ARI.ARI(kwargs).encode)))
		self.btnHUFF = tk.Button(self, height=2, width=30, text=Constants.HUFFMAN_ENCODING, command=self.transform_selected(WidgetInformation("Huffman Compression", TYPE_BYTES, TYPE_BYTES, lambda **kwargs: Huffman.Huffman(kwargs).encode)))
		self.parameterInput = ParameterInput(self)
	def display_transforms_for_type(self, inType, outType):

		self.btnJPEG.pack_forget()
		self.btnDIT.pack_forget()
		self.btnRGB.pack_forget()
		self.btnYUV.pack_forget()
		self.btnGreyscale.pack_forget()
		self.btnColorQuantization.pack_forget()

		self.btnLZW.pack_forget()
		self.btnRLE.pack_forget()
		self.btnARI.pack_forget()
		self.btnHUFF.pack_forget()

		# Make buttons asking for compression types
		if (inType == TYPE_BITMAP or inType == None) or (outType == TYPE_ENCODED or outType == None):
			self.btnJPEG.pack(side = "left")#(relx=.25, rely=0.69, anchor='n')

		if (inType == TYPE_BYTES or inType == None) or (outType == TYPE_BYTES or outType == None):
			self.btnLZW.pack(side = "left")#place(relx=.25, rely=0.75, anchor='n')

			self.btnRLE.pack(side = "left")#place(relx=.25, rely=0.81, anchor='n')

			self.btnARI.pack(side = "left")#place(relx=.25, rely=0.87, anchor='n')

			self.btnHUFF.pack(side = "left")#place(relx=.25, rely=0.93, anchor='n')
		if (inType == TYPE_BITMAP or inType == None) or (outType == TYPE_BITMAP or outType == None):
			self.btnDIT.pack(side = "left")
			self.btnColorQuantization.pack(side = "left")
			self.btnRGB.pack(side = "left")
			self.btnYUV.pack(side="left")
			self.btnGreyscale.pack(side="left")

	# Function for handling when a button is pressed
	def transform_selected(self, widgetInformation, parameters = {}, displayNames = {}):
		def handler():
			self.selected_label['text'] = "Selected: " + widgetInformation.name
			self.selected = widgetInformation
			self.parameterInput.setParameters(parameters, displayNames)
		return handler



