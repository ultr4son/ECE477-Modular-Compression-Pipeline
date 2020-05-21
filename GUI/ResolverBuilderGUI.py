#GUI that reads in a file and determines what type of transforms can be done on it

import string
import sys
import numpy as np
import tkinter as tk
import math
from Transform.TransformState import State

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog	# used to be named tkFileDialog		
import cv2 as cv
import imghdr
import os.path


from GUI.Common import *
from Transform.TransformSystem import runTransformations


matchType = 0
CONTROL_ROW = 0
TRANSFORM_ROW = 1

RUN_BUTTON_COLUMN = 0
IMPORT_BMP_COLUMN = 1
IMPORT_TEXT_COLUMN = 2
IMPORT_IMAGE_COLUMN = 3
ADD_COLUMN = 4


class Builderwindow(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.transforms = []
        self.initialValue = None
        self.initialType = None
        self.create_widgets()


    def insertTransform(self, position, name, inType, outType, transformFunction):
        transformWidget = TransformWidget(self, name = name, inType = inType, outType = outType, transform = transformFunction)
        insertBeforeFrame = tk.Frame(self)

        insertBeforeFrame.bind("<Button-1>", )
        transformWidget.grid(column = position + 1, row=TRANSFORM_ROW)
        self.transforms.append(transformWidget)

    def create_widgets(self):
        self.runButton = tk.Button(self, text = "Run", command = self.handleRun)
        self.runButton.grid(row = CONTROL_ROW, column = RUN_BUTTON_COLUMN)
        self.runButton["state"] = "disabled"

        self.importBMPButton = tk.Button(self, text = "Import Bitmap", command = self.handleImportBMP)
        self.importBMPButton.grid(row = CONTROL_ROW, column = IMPORT_BMP_COLUMN)

        self.importTextButton = tk.Button(self, text = "Import Text", command = self.handleImportText)
        self.importTextButton.grid(row = CONTROL_ROW, column = IMPORT_TEXT_COLUMN)

        self.importImgButton = tk.Button(self, text = "Import Image", command = self.handleImportImage)
        self.importImgButton.grid(row = CONTROL_ROW, column = IMPORT_IMAGE_COLUMN)

        self.addTransformButton = tk.Button(self, text = "Add Transform", command = self.handleAddTransform)
        self.addTransformButton.grid(row = CONTROL_ROW, column = ADD_COLUMN)




    def dnd_accept(self, target ,event):
        return self
    def dnd_motion(self, source, event):
        pass
    def dnd_enter(self, target, event):
        pass
    def dnd_commit(self, source: TransformWidget, event):

        x, y = source.winfo_pointerxy()
        target = self.getContainingTransormWidget(source.winfo_containing(x, y))

        sourceIndex = self.transforms.index(source)
        targetIndex = self.transforms.index(target)

        source.grid_forget()
        target.grid_forget()

        source.grid(column = targetIndex, row = TRANSFORM_ROW)
        target.grid(column = sourceIndex, row = TRANSFORM_ROW)

        self.transforms[sourceIndex], self.transforms[targetIndex] = target, source

    def dnd_leave(self, source, event):
        pass
    def getContainingTransormWidget(self, source):
        while not isinstance(source, TransformWidget):
            source = source.master
        return source

    def handleImportBMP(self):
        fileName = filedialog.askopenfilename(title = "Select a bitmap file", filetypes = [("JPEG", "*.jpg"), ("Bitmap", "*.bmp")])
        self.initialValue = cv.imread(fileName)
        self.initialType = TYPE_BITMAP
        self.runButton["state"] = "normal"

    def handleImportImage(self):
        fileName = filedialog.askopenfilename(title = "Select a bitmap file", filetypes = [("JPEG", "*.jpg"), ("Bitmap", "*.bmp")])
        self.initialValue = cv.imread(fileName)
        self.initialType = TYPE_ENCODED
        self.runButton["state"] = "normal"

    def handleImportText(self):
        file = filedialog.askopenfile(title = "Select a text file", mode="r", filetypes = [("Text", "*.txt"), ("All", "*.*")])
        self.initialValue = file.read()
        self.initialType = TYPE_BYTES
        self.runButton["state"] = "normal"

    def handleRun(self):
        if self.initialValue is not None:
            (_, states) = runTransformations([widget.transform for widget in self.transforms], self.initialValue)
            #TODO: put call to output window here
    def handleAddTransform(self):
        self.resolverWindow = Tk()
        self.resolverWindow.geometry("500x700+10+60")
        panelA = None

        # Transform Buttons
        btnJPEG = Button(self.resolverWindow, height=2, width=30, text="JPEG Compression", command=self.JpegSelected)
        btnJPEG.place(relx=.25, rely=0.69, anchor='n')

        btnLZW = Button(self.resolverWindow, height=2, width=30, text="LZW Compression", command=self.LZWSelected)
        btnLZW.place(relx=.25, rely=0.75, anchor='n')

        btnRLE = Button(self.resolverWindow, height=2, width=30, text="Run Length Encoding", command=self.RLESelected)
        btnRLE.place(relx=.25, rely=0.81, anchor='n')

        btnARI = Button(self.resolverWindow, height=2, width=30, text="Arithmetic Encoding", command=self.ARISelected)
        btnARI.place(relx=.25, rely=0.87, anchor='n')

        btnHUFF = Button(self.resolverWindow, height=2, width=30, text="Huffman Encoding", command=self.HuffSelected)
        btnHUFF.place(relx=.25, rely=0.93, anchor='n')

        btnSUB = Button(self.resolverWindow, height=2, width=30, text="Subsampling", command=self.SubSelected)
        btnSUB.place(relx=.75, rely=0.69, anchor='n')

        btnQUANT = Button(self.resolverWindow, height=2, width=30, text="Quantization", command=self.QuantSelected)
        btnQUANT.place(relx=.75, rely=0.75, anchor='n')

        btnDIT = Button(self.resolverWindow, height=2, width=30, text="Dithering", command=self.DitSelected)
        btnDIT.place(relx=.75, rely=0.81, anchor='n')

        btnCOL = Button(self.resolverWindow, height=2, width=30, text="Color Space Changer", command=self.ColSelected)
        btnCOL.place(relx=.75, rely=0.87, anchor='n')

        btnRES = Button(self.resolverWindow, height=2, width=30, text="Exit", command=self.exitResolver)
        btnRES.place(relx=.75, rely=0.93, anchor='n')

        # T1 - Displays image information
        T1 = tk.Text(self.resolverWindow, height=15, width=25)
        T1.pack(side="right", padx="10", pady="10")
        T1.insert(tk.END, "    Image information")
        T1.place(relx=.77, rely=0.275, anchor='n')


        # T2 - Display 'Available Transformations'
        T2 = tk.Text(self.resolverWindow, height=1, width=59)
        T2. pack(side="left", padx="10", pady="10")
        T2.insert(tk.END, "                Available Transformations:     ")
        T2.place(relx=.50, rely=0.65, anchor='n')

    #Functions for handling resolver self.resolverWindow buttons
    def JpegSelected(self):
        print("JPEG Compression selected")

    def LZWSelected(self):
        print("LZW Compression selected")

    def RLESelected(self):
        print("Run Length Encoding selected")

    def ARISelected(self):
        print("Arithmetic Encoding selected")

    def HuffSelected(self):
        print("Huffman encoding selected")

    def SubSelected(self):
        print("Subsampling selected")

    def QuantSelected(self):
        print("Quantization selected")

    def DitSelected(self):
        print("Dithering selected")

    def ColSelected(self):
        print("Color Space Changer selected")

    def exitResolver(self):
    	self.resolverWindow.destroy()



# initialize the window toolkit along with the image panel
if __name__ == '__main__':

	root = Tk()
	root.geometry("362x26+550+60")
	app = Builderwindow(root)

	# kick off the GUI
	root.mainloop()