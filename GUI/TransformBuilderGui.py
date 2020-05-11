import tkinter as tk
import tkinter.filedialog as filedialog
import cv2 as cv
from GUI.Common import *
from Transform.TransformSystem import runTransformations
from GUI.outputview import *
import Transform.TransformExample

CONTROL_ROW = 0
TRANSFORM_ROW = 1

RUN_BUTTON_COLUMN = 0
IMPORT_IMAGE_COLUMN = 1
IMPORT_TEXT_COLUMN = 2
ADD_COLUMN = 3

class BuilderWindow(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.transforms = []
        self.initialValue = None
        self.initialType = None
        self.create_widgets()
    def insertAt(self, position):
        def handler(self):
            #TODO: call resolver
            self.insertTransform(position + 1, )
            pass
        return handler


    def insertTransform(self, transformPosition, name, inType, outType, transformFunction):
        widget = TransformWidget(self, name, inType, outType, transformFunction)
        widget.insertBeforeButton.command = self.insertAt(transformPosition - 1)
        widget.insertAfterButton.command = self.insertAt(transformPosition + 1)
        widget.grid(row = TRANSFORM_ROW, column = transformPosition - 1)
        self.transforms.insert(transformPosition - 1, widget)


    def create_widgets(self):
        self.runButton = tk.Button(self, text = "Run", command = self.handleRun)
        self.runButton.grid(row = CONTROL_ROW, column = RUN_BUTTON_COLUMN)

        #TODO: testing code remove later
        transformFunction1 = Transform.TransformExample.ThompsonImageCompression(2).transform
        transformFunction2 = Transform.TransformExample.ThompsonImageCompression(2, 1).transform
        self.insertTransform(1, "Test", "bitmap", "bitmap", transformFunction1)
        self.insertTransform(2, "Test2", "bitmap", "bitmap", transformFunction2)
        self.initialValue = cv.imread("../Transform/burmese.jpg")
        #

        # self.importImageButton = tk.Button(self, text = "Import Bitmap", command = self.handleImportImage)
        # self.importImageButton.grid(row = CONTROL_ROW, column = IMPORT_IMAGE_COLUMN)
        #
        # self.importTextButton = tk.Button(self, text = "Import Text", command = self.handleImportText)
        # self.importTextButton.grid(row = CONTROL_ROW, column = IMPORT_TEXT_COLUMN)

        # self.addTransformButton = tk.Button(self, text = "Add Selected Transform", command = self.handleAddTransform)
        # self.addTransformButton.grid(row = CONTROL_ROW, column = ADD_COLUMN)




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

    # def handleImportImage(self):
    #     fileName = filedialog.askopenfilename(title = "Select a bitmap file", filetypes = [("JPEG", "*.jpg"), ("Bitmap", "*.bmp")])
    #     self.initialValue = cv.imread(fileName)
    #     self.initialType = TYPE_BITMAP
    #     self.runButton["state"] = "normal"
    #
    # def handleImportText(self):
    #     file = filedialog.askopenfile(title = "Select a text file", mode="r", filetypes = [("Text", "*.txt"), ("All", "*.*")])
    #     self.initialValue = file.read()
    #     self.initialType = TYPE_BYTES
    #     self.runButton["state"] = "normal"

    def handleRun(self):
        if self.initialValue is not None:
            (_, states) = runTransformations([widget.transform for widget in self.transforms], self.initialValue)
            newWindow = tk.Toplevel(self.master)
            outputWindow = Window(newWindow)
            outputWindow.outputFunc(states)
        
    # def handleAddTransform(self):
    #     #TODO: put call to transform window here
    #     pass

if __name__ == '__main__':
    root = tk.Tk()
    app = BuilderWindow(root)
    root.mainloop()