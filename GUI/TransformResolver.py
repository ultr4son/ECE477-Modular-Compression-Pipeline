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
import TypeChange

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
		self.grid()
		T2 = tk.Label(self, height=1, width=59, text = "Avaliable Transformations")
		T2.grid(row = 0, column = 0, columnspan = 2)#pack(side="top")#place(side="left", padx="10", pady="10")
		self.selected_label = tk.Label(self, height = 1, width = 59, text = "Selected: ")
		self.selected_label.grid(row = 1, column = 0, columnspan =2 )#.pack(side = "top")

		self.inputLabel = tk.Label(self, height = 1, width = 30, text = "Generates")
		self.inputLabel.grid(row = 4, column = 0)

		self.outputLabel = tk.Label(self, height = 1, width = 30, text = "Recives")
		self.outputLabel.grid(row = 4, column = 1)

		self.init_widgets()
		self.selected = None
		# T2.insert(tk.END, "                Available Transformations:     ")
		# T2.place(relx=.50, rely=0.65, anchor='n')
	def init_widgets(self):

		self.btnJPEG = tk.Button(self, height=2, width=30, text=Constants.JPEG_ENCODING,
								 command=self.transform_selected(
									 WidgetInformation(Constants.JPEG_ENCODING, TYPE_BITMAP, TYPE_ENCODED,
													   lambda kwargs: JPEG.Jpeg(**kwargs).encode),
									 get_default_args(JPEG.Jpeg), {"quality": "Quality"}))

		self.btnJPEGDecode = tk.Button(self, height=2, width=30, text=Constants.JPEG_DECODING,
									   command=self.transform_selected(
										   WidgetInformation(Constants.JPEG_DECODING, TYPE_ENCODED, TYPE_BITMAP,
															 lambda kwargs: JPEG.Jpeg(**kwargs).decode)))

		self.btnDIT = tk.Button(self, height=2, width=30, text=Constants.DITHERING, command=self.transform_selected(
			WidgetInformation(Constants.DITHERING, TYPE_BITMAP, TYPE_BITMAP,
							  lambda kwargs: DIT.Dither(**kwargs).encode), get_default_args(DIT.Dither),
			{"ditherVal": "Dither Amount"}))

		self.btnRGB = tk.Button(self, height=2, width=30, text=Constants.RGB, command=self.transform_selected(
			WidgetInformation(Constants.RGB, TYPE_BITMAP, TYPE_BITMAP,
							  lambda kwargs: color_space.Color_Space(**kwargs).RGB)))

		self.btnYUV = tk.Button(self, height=2, width=30, text=Constants.YUV, command=self.transform_selected(
			WidgetInformation(Constants.YUV, TYPE_BITMAP, TYPE_BITMAP,
							  lambda kwargs: color_space.Color_Space(**kwargs).YUV)))

		self.btnGreyscale = tk.Button(self, height=2, width=30, text=Constants.GREYSCALE,
									  command=self.transform_selected(
										  WidgetInformation(Constants.GREYSCALE, TYPE_BITMAP, TYPE_BITMAP,
															lambda kwargs: color_space.Color_Space(**kwargs).Gray)))

		self.btnColorQuantization = tk.Button(self, height=2, width=30, text=Constants.COLOR_QUANTIZATION,
											  command=self.transform_selected(
												  WidgetInformation(Constants.COLOR_QUANTIZATION, TYPE_BITMAP,
																	TYPE_BITMAP,
																	lambda kwargs: color_quantization.Color_Quantizaion(
																		**kwargs).kmeans_quantization), get_default_args(color_quantization.Color_Quantizaion), {"K": "Colors"}))

		self.btnLZW = tk.Button(self, height=2, width=30, text=Constants.LZW_ENCODING, command=self.transform_selected(
			WidgetInformation(Constants.LZW_ENCODING, TYPE_BYTES, TYPE_BYTES, lambda kwargs: LZW.LZW(**kwargs).encode)))

		self.btnLZWDecoding = tk.Button(self, height=2, width=30, text=Constants.LZW_DECODING, command=self.transform_selected(
			WidgetInformation(Constants.LZW_DECODING, TYPE_BYTES, TYPE_BYTES, lambda kwargs: LZW.LZW(**kwargs).decode)))

		self.btnRLE = tk.Button(self, height=2, width=30, text=Constants.RUN_LENGTH_ENCODING,
								command=self.transform_selected(
									WidgetInformation(Constants.RUN_LENGTH_ENCODING, TYPE_BYTES, TYPE_BYTES,
													  lambda kwargs: RLE.RLE(**kwargs).encode)))

		self.btnRLEDecoding = tk.Button(self, height=2, width=30, text=Constants.RUN_LENGTH_DECODING,
								command=self.transform_selected(
									WidgetInformation(Constants.RUN_LENGTH_DECODING, TYPE_BYTES, TYPE_BYTES,
													  lambda kwargs: RLE.RLE(**kwargs).decode)))

		self.btnARI = tk.Button(self, height=2, width=30, text=Constants.ARITHMETIC_CODING,
								command=self.transform_selected(
									WidgetInformation(Constants.ARITHMETIC_CODING, TYPE_BYTES, TYPE_BYTES,
													  lambda kwargs: ARI.ARI(**kwargs).encode)))
		self.btnHUFF = tk.Button(self, height=2, width=30, text=Constants.HUFFMAN_ENCODING,
								 command=self.transform_selected(
									 WidgetInformation(Constants.HUFFMAN_ENCODING, TYPE_BYTES, TYPE_BYTES,
													   lambda kwargs: Huffman.Huffman(**kwargs).encode)))
		self.btnHUFFDecoding = tk.Button(self, height=2, width=30, text= Constants.HUFFMAN_DECODING,
								 command=self.transform_selected(
									 WidgetInformation(Constants.HUFFMAN_DECODING, TYPE_BYTES, TYPE_BYTES,
													   lambda kwargs: Huffman.Huffman(**kwargs).decode)))

		self.btnBitmapToBytes = tk.Button(self, height=2, width=30, text="Bitmap to Bytes",
										  command=self.transform_selected(
											  WidgetInformation("Bitmap to Bytes", TYPE_BITMAP, TYPE_BYTES,
																lambda kwargs: TypeChange.BitmapToBytes(
																	**kwargs).encode)))

		self.btnBytesToBitmap = tk.Button(self, height=2, width=30, text="Bytes to Bitmap",
										  command=self.transform_selected(
											  WidgetInformation("Bytes to Bitmap", TYPE_BYTES, TYPE_BITMAP,
																lambda kwargs: TypeChange.BytesToBitmap(
																	**kwargs).encode),
											  get_default_args(TypeChange.BytesToBitmap), {"aspect": "Aspect Ratio"}))

		self.parameterInput = ParameterInput.ParameterInput(self)
		self.parameterInput.grid(row = 3, column = 0, columnspan = 2)
		# self.parameterInput.pack(side = "bottom")
		self.inputDictionary = {
			TYPE_BYTES: [ self.btnLZW,
						  self.btnLZWDecoding,
						  self.btnRLE,
						  self.btnRLEDecoding,
						  self.btnARI,
			     		  self.btnHUFF,
						  self.btnHUFFDecoding,
						  self.btnBytesToBitmap ],
			TYPE_BITMAP: [
					self.btnDIT,
					self.btnColorQuantization,
					self.btnRGB,
					self.btnYUV,
					self.btnGreyscale,
					self.btnBitmapToBytes,
					self.btnJPEG
					 ],
			TYPE_ENCODED: [
				self.btnJPEG
			]
		}
		self.outputDictionary = {
			TYPE_BYTES: [ self.btnLZW,
						  self.btnLZWDecoding,
						  self.btnRLE,
						  self.btnRLEDecoding,
						  self.btnARI,
			     		  self.btnHUFF,
						  self.btnHUFFDecoding,
						  self.btnBytesToBitmap],
			TYPE_BITMAP: [
				self.btnDIT,
				self.btnColorQuantization,
				self.btnRGB,
				self.btnYUV,
				self.btnGreyscale,
				self.btnBitmapToBytes,
				self.btnJPEG],
			TYPE_ENCODED: [
				self.btnJPEGDecode
			]
		}
	def display_transforms_for_type(self, inType, outType):
		# for
		# self.btnJPEG.grid_forget()
		# self.btnDIT.grid_forget()
		# self.btnRGB.grid_forget()
		# self.btnYUV.grid_forget()
		# self.btnGreyscale.grid_forget()
		# self.btnColorQuantization.grid_forget()
		#
		# self.btnLZW.grid_forget()
		# self.btnRLE.grid_forget()
		# self.btnARI.grid_forget()
		# self.btnHUFF.grid_forget()
		for li in self.inputDictionary.values():
			for t in li:
				t.grid_forget()
		for li in self.outputDictionary.values():
			for t in li:
				t.grid_forget()
		row = 5
		if(inType in self.inputDictionary and outType in self.outputDictionary):
			sameTypeTransforms = list(set(self.inputDictionary[inType]) & set(self.outputDictionary[outType]))
			for t in sameTypeTransforms:
				t.grid(column = 0, row = row, columnspan = 2, sticky = "ew")
				row += 1
			inputRow = row
			uniqueInputs = list(set(self.inputDictionary[inType]) - set(sameTypeTransforms))
			for t in uniqueInputs:
				t.grid(column = 0, row = inputRow, columnspan = 1)
				inputRow += 1

			outputRow = row
			uniqueOutputs = list(set(self.outputDictionary[outType]) - set(sameTypeTransforms))
			for t in uniqueOutputs:
				t.grid(column = 1, row = outputRow, columnspan = 1)
				outputRow += 1
		elif inType in self.inputDictionary:
			for t in self.inputDictionary[inType]:
				t.grid(column = 0, row = row)
				row += 1
		elif outType in self.outputDictionary:
			for t in self.outputDictionary[outType]:
				t.grid(column = 1, row = row)
				row += 1
		else:
			for li in self.inputDictionary.values():
				for t in li:
					t.grid(column = 0, row = row, columnspan = 2, sticky="ew")
					row += 1
			for li in self.outputDictionary.values():
				for t in li:
					t.grid(column = 0, row = row, columnspan = 2, sticky="ew")
					row += 1

		# # Make buttons asking for compression types
		# if (inType == TYPE_ENCODED or inType == None):
		# 	self.btnJPEG.grid(row = row, column = 0)#pack(side = "left")#(relx=.25, rely=0.69, anchor='n')
		# 	row += 1
		# if (outType == TYPE_ENCODED or outType == None):
		# 	self.btnJPEGDecode.grid(row = row, column = 1)
		# 	row += 1
		#
		# if (inType == TYPE_BYTES or inType == None and outType == TYPE_BYTES or outType == None):
		# 	self.btnLZW.pack(row = row, column)#place(relx=.25, rely=0.75, anchor='n')
		#
		# 	self.btnRLE.pack(side = "left")#place(relx=.25, rely=0.81, anchor='n')
		#
		# 	self.btnARI.pack(side = "left")#place(relx=.25, rely=0.87, anchor='n')
		#
		# 	self.btnHUFF.pack(side = "left")#place(relx=.25, rely=0.93, anchor='n')
		# 	self.btnBytesToBitmap.pack(side = "left")
		# if (inType == TYPE_BITMAP or inType == None):
		# 	self.btnDIT.pack(side = "left")
		# 	self.btnColorQuantization.pack(side = "left")
		# 	self.btnRGB.pack(side = "left")
		# 	self.btnYUV.pack(side="left")
		# 	self.btnGreyscale.pack(side="left")
		# 	self.btnBitmapToBytes.pack(side="left")

	# Function for handling when a button is pressed
	def transform_selected(self, widgetInformation, parameters = {}, displayNames = {}):
		def handler():
			self.selected_label['text'] = "Selected: " + widgetInformation.name
			self.selected = widgetInformation
			self.parameterInput.setParameters(parameters, displayNames)
		return handler



