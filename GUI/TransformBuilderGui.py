import tkinter as tk
import tkinter.filedialog as filedialog
import cv2 as cv
from GUI.Common import *
from Transform.TransformSystem import runTransformations
from GUI.outputview import *
import Transform.TransformExample
import GUI.TransformResolver as tr
import LZW
from functools import *

CONTROL_ROW = 0
TRANSFORM_ROW = 1

RUN_BUTTON_COLUMN = 0
IMPORT_IMAGE_COLUMN = 1
IMPORT_TEXT_COLUMN = 2
ADD_COLUMN = 3
REMOVE_SELECTED_COLUMN = 4


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
    def handleInstertAtLocation(self, insertWidget, before):
        def handler():
            if self.resolver.selected is not None:
                selected = self.resolver.selected
                self.insertTransform(insertWidget, before, selected.name, selected.inType, selected.outType, selected.transformInitializer(self.resolver.parameterInput.parameters))
        return handler

    def draw_state(self):
        # for w in self.transforms:
        #     w.grid_forget()
        self.updateRunState()
        if len(self.transforms) == 0 and self.initialWidget is None:
            self.initialAddButton.grid(row=TRANSFORM_ROW, column=0, sticky="nsew", columnspan=5)
            self.resolver.display_transforms_for_type(None, None)
        else:
            self.initialAddButton.grid_forget()
        c = 0

        if self.initialWidget is not None:
            self.initialWidget.grid(row = TRANSFORM_ROW, column = 0)
            c = 1
        for w in self.transforms:
            w.grid(row = TRANSFORM_ROW, column = c)
            c += 1
    def insertTransform(self, insertWidget, before, name, inType, outType, transformFunction):

        widget = TransformWidget(self, name = name, inType= inType, outType= outType, transform= transformFunction, resolver= self.resolver)
        widget.bind_class(widget.tag(), "<Button-1>", self.handleWidgetClick)
        widget.insertBeforeButton['command'] = self.handleInstertAtLocation(widget, True)
        widget.insertAfterButton['command'] = self.handleInstertAtLocation(widget, False)
        if insertWidget:
            index = self.transforms.index(insertWidget)
            if before:
                self.transforms.insert(index, widget)
            else:
                self.transforms.insert(index + 1, widget)
        else:
            self.transforms.insert(0, widget)
        self.draw_state()


    def handleWidgetClick(self, event):
        transform = findParent(event.widget, TransformWidget)
        self.resolver.display_transforms_for_type(transform.inType, transform.outType)
        transform.focus()
        self.selectedTransform = transform
        if not transform.static:
            dnd.dnd_start(transform, event)

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
        self.initialAddButton.grid(row = TRANSFORM_ROW, column = 0, sticky= "nsew", columnspan=5)

        self.importImageButton = tk.Button(self, text = "Import Bitmap", command = self.handleImportImage)
        self.importImageButton.grid(row = CONTROL_ROW, column = IMPORT_IMAGE_COLUMN)

        self.importTextButton = tk.Button(self, text = "Import Text", command = self.handleImportText)
        self.importTextButton.grid(row = CONTROL_ROW, column = IMPORT_TEXT_COLUMN)

        self.deleteButton = tk.Button(self, text = "Remove Selected", command = self.handleRemoveSelected)
        self.deleteButton.grid(row = CONTROL_ROW, column = REMOVE_SELECTED_COLUMN)

        # self.addTransformButton = tk.Button(self, text = "Add Selected Transform", command = self.handleAddTransform)
        # self.addTransformButton.grid(row = CONTROL_ROW, column = ADD_COLUMN)
        newWindow = tk.Toplevel(self.master)
        self.resolver = tr.TransformResolver(newWindow)
        self.resolver.display_transforms_for_type(None, None)
        self.updateRunState()
    def initialAdd(self):
        if self.resolver.selected is not None:
            self.initialAddButton.grid_forget()
            self.handleInstertAtLocation(None, False)()
            self.resolver.display_transforms_for_type(self.resolver.selected.inType, self.resolver.selected.outType)

    def dnd_accept(self, target ,event):
        return self
    def dnd_motion(self, source, event):
        pass
    def dnd_enter(self, target, event):
        pass
    def dnd_commit(self, source: TransformWidget, event):

        x, y = source.winfo_pointerxy()
        target = findParent(source.winfo_containing(x, y), TransformWidget)

        sourceIndex = self.transforms.index(source)
        targetIndex = self.transforms.index(target)

        self.transforms[sourceIndex], self.transforms[targetIndex] = target, source
        self.draw_state()

    def dnd_leave(self, source, event):
        pass

    def handleImportImage(self):
        fileName = filedialog.askopenfilename(title = "Select a bitmap file", filetypes = [("JPEG", "*.jpg"), ("Bitmap", "*.bmp")])
        self.initialValue = cv.imread(fileName)
        self.initialType = TYPE_BITMAP
        self.initialWidget = TransformWidget(self, "Image File", TYPE_NIL, TYPE_BITMAP, self.resolver, None)
        self.initialWidget.static = True
        self.initialWidget.insertAfterButton['command'] = self.handleInstertAtLocation(None, False)

        self.draw_state()
        self.resolver.display_transforms_for_type(self.initialType, TYPE_NIL)

    def handleRemoveSelected(self):
        if self.selectedTransform is not None:
            self.selectedTransform.grid_forget()
            self.transforms.remove(self.selectedTransform)
            self.selectedTransform.destroy()
            self.draw_state()


    def handleImportText(self):
        file = filedialog.askopenfile(title = "Select a text file", mode="r", filetypes = [("Text", "*.txt"), ("All", "*.*")])
        self.initialValue = file.read()
        self.initialType = TYPE_BYTES
        self.initialWidget = TransformWidget(self, "Text File", TYPE_NIL, TYPE_BYTES, self.resolver, None)
        self.initialWidget.insertAfterButton['command'] = self.handleInstertAtLocation(None,False)

        self.draw_state()
        self.initialWidget.static = True
        self.resolver.display_transforms_for_type(self.initialType, TYPE_NIL)

    def updateRunState(self):
        self.runButton["state"] = "normal" if self.validSystem() and self.initialValue is not None else "disable"

    def validSystem(self):
        currentOutType = self.initialType
        for t in self.transforms:
            if t.inType != currentOutType:
                return False
            currentOutType = t.outType
        return True

    def handleRun(self):
        if self.initialValue is not None:
            if self.validSystem():
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