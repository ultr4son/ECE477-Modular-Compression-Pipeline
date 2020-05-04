import tkinter as tk
from GUI.Common import *
import decimal

CONTROL_ROW = 0
TRANSFORM_ROW = 1


class BuilderWindow(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.transforms = []

        self.create_widgets()

    def create_widgets(self):
        for i in range(0, 5):
            transformWidget = TransformWidget(self, name="Test " + str(i), inType=TYPE_BYTES, outType=TYPE_BYTES)
            transformWidget.grid(column = i, row = TRANSFORM_ROW)
            self.transforms.append(transformWidget)

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


        self.transforms[sourceIndex], self.transforms[targetIndex]= target, source

    def dnd_leave(self, source, event):
        pass
    def getContainingTransormWidget(self, source):
        while not isinstance(source, TransformWidget):
            source = source.master
        return source

if __name__ == '__main__':
    root = tk.Tk()
    app = BuilderWindow(root)
    root.mainloop()