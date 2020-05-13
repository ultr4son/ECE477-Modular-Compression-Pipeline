import tkinter as tk
import tkinter.filedialog as filedialog
import cv2 as cv
from GUI.Common import *
from Transform.TransformSystem import runTransformations
from GUI.outputview import *
import Transform.TransformExample
import GUI.TransformResolver as tr
import LZW
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
        self.initialWidget = None
        self.initialValue = None
        self.initialType = None

        self.create_widgets()
    def insertAt(self, position):
        def handler():
            if self.resolver.selected is not None:
                selected = self.resolver.selected
                self.insertTransform(position, selected.name, selected.inType, selected.outType, selected.function)
        return handler

    def regrid_transforms(self):
        # for w in self.transforms:
        #     w.grid_forget()
        self.initialAddButton.grid_forget()
        c = 0
        if self.initialWidget is not None:
            self.initialWidget.grid(row = TRANSFORM_ROW, column = 0)
            c = 1

        for w in self.transforms:
            w.grid(row = TRANSFORM_ROW, column = c)
            c += 1
    def insertTransform(self, transformPosition, name, inType, outType, transformFunction):

        widget = TransformWidget(self, name = name, inType= inType, outType= outType, transform= transformFunction, resolver= self.resolver)

        widget.insertBeforeButton['command'] = self.insertAt(transformPosition)
        widget.insertAfterButton['command'] = self.insertAt(transformPosition + 1)
        self.transforms.insert(transformPosition, widget)
        self.regrid_transforms()



    def create_widgets(self):
        self.runButton = tk.Button(self, text = "Run", command = self.handleRun)
        self.runButton.grid(row = CONTROL_ROW, column = RUN_BUTTON_COLUMN)

        # lzwTransform = LZW.LZW().encode
        # transformFunction1 = Transform.TransformExample.ThompsonImageCompression(2).transform
        # transformFunction2 = Transform.TransformExample.ThompsonImageCompression(2, 1).transform
        # self.insertTransform(1, "Test", TYPE_BITMAP, TYPE_BITMAP, transformFunction1)
        # self.insertTransform(2, "Test2", TYPE_BITMAP, TYPE_BITMAP, transformFunction2)
        # self.insertTransform(3, "LZW", TYPE_BYTES, TYPE_BYTES, lzwTransform)
        # self.initialValue = cv.imread("../Transform/burmese.jpg")
        #
        self.initialAddButton = tk.Button(self, text = "+", command = self.initialAdd)
        self.initialAddButton.grid(row = TRANSFORM_ROW, column = 0, sticky= "nsew", columnspan=4)

        self.importImageButton = tk.Button(self, text = "Import Bitmap", command = self.handleImportImage)
        self.importImageButton.grid(row = CONTROL_ROW, column = IMPORT_IMAGE_COLUMN)

        self.importTextButton = tk.Button(self, text = "Import Text", command = self.handleImportText)
        self.importTextButton.grid(row = CONTROL_ROW, column = IMPORT_TEXT_COLUMN)

        # self.addTransformButton = tk.Button(self, text = "Add Selected Transform", command = self.handleAddTransform)
        # self.addTransformButton.grid(row = CONTROL_ROW, column = ADD_COLUMN)
        newWindow = tk.Toplevel(self.master)
        self.resolver = tr.TransformResolver(newWindow)
        self.resolver.select_transform(None, None)
    def initialAdd(self):
        if self.resolver.selected is not None:
            self.initialAddButton.grid_forget()
            self.insertAt(0)()

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

        self.transforms[sourceIndex], self.transforms[targetIndex] = target, source
        self.regrid_transforms()

    def dnd_leave(self, source, event):
        pass
    def getContainingTransormWidget(self, source):
        while not isinstance(source, TransformWidget):
            source = source.master
        return source

    def handleImportImage(self):
        fileName = filedialog.askopenfilename(title = "Select a bitmap file", filetypes = [("JPEG", "*.jpg"), ("Bitmap", "*.bmp")])
        self.initialValue = cv.imread(fileName)
        self.initialType = TYPE_BITMAP
        self.initialWidget = TransformWidget(self, "Image File", TYPE_NIL, TYPE_BITMAP, self.resolver, None)
        self.initialWidget.static = True
        self.initialWidget.insertAfterButton['command'] = self.insertAt(1)

        self.regrid_transforms()
        self.resolver.select_transform(self.initialType, TYPE_NIL)


    def handleImportText(self):
        file = filedialog.askopenfile(title = "Select a text file", mode="r", filetypes = [("Text", "*.txt"), ("All", "*.*")])
        self.initialValue = file.read()
        self.initialType = TYPE_BYTES
        self.initialWidget = TransformWidget(self, "Text File", TYPE_NIL, TYPE_BYTES, self.resolver, None)
        self.initialWidget.insertAfterButton['command'] = self.insertAt(1)

        self.regrid_transforms()
        self.initialWidget.static = True
        self.resolver.select_transform(self.initialType, TYPE_NIL)

    def handleRun(self):
        if self.initialValue is not None:
            (_, states) = runTransformations([widget.transform for widget in self.transforms], self.initialValue)
            newWindow = tk.Toplevel(self.master)
            outputWindow = Window(newWindow)
            outputWindow.outputFunc(states, self)
        
    # def handleAddTransform(self):
    #     #TODO: put call to transform window here
    #     pass

if __name__ == '__main__':
    root = tk.Tk()
    app = BuilderWindow(root)
    root.mainloop()