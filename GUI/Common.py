import tkinter as tk
import uuid
import tkinter.dnd as dnd

TYPE_BITMAP = "bitmap"
TYPE_BYTES = "bytes"
TYPE_JPEG = "jpeg"

TYPE_COLOR = {
    TYPE_BITMAP: "light blue",
    TYPE_BYTES: "purple",
    TYPE_JPEG: "green"
}

def colorForType(type):
    if type in TYPE_COLOR:
        return TYPE_COLOR[type]
    return "white"
def bindForWidget(tag, widget):
    widget.bindtags((tag, ) + widget.bindtags())

class ConnectWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        arrowCanvas = tk.Canvas(self, width = 20, height = 30)
        arrowCanvas.pack()
        arrowCanvas.create_line(0, 15, 20, 15, arrow = tk.LAST)

    def dnd_accept(self, target, event):
        print("accept connect")
        #return self

    def dnd_motion(self, source, event):
        print("motion connect")
        pass

    def dnd_enter(self, target, event):
        print("enter connect")
        pass

    def dnd_commit(self, source, event):
        print("commit connect")
        pass
    def dnd_leave(self, source, event):
        pass


class TypeWidget(tk.Frame):
    def __init__(self, master=None, typeName = "", color = "white"):
        super().__init__(master)
        self.master = master
        self.type = typeName
        self.color = color
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.typeText = tk.Label(self,text = self.type, bg = self.color, width = 7, height = 3)
        self.typeText.pack()

class TransformWidget(tk.Frame):
    def __init__(self, master = None, name = "", inType = "", outType = "", transform = None):
        super().__init__(master)
        self.master = master
        self.inType = inType
        self.outType = outType
        self.name = name
        self.id = str(uuid.uuid4())
        self.transform = transform

        self.bind_class(self.tag(), "<Button-1>", self.clickEvent)
        self.config(highlightthickness=2)
        self.grid()
        self.create_widgets()

    def tag(self):
        return self.__class__.__name__ + self.id

    def create_widgets(self):

        self.inTypeWidget = TypeWidget(self, self.inType, colorForType(self.inType))
        self.inTypeWidget.pack(side="left")
        bindForWidget(self.tag(), self.inTypeWidget)

        self.outTypeWidget = TypeWidget(self, self.outType, colorForType(self.outType))
        self.outTypeWidget.pack(side="right")
        bindForWidget(self.tag(), self.outTypeWidget)

        self.nameWidget = tk.Label(self, text = self.name, width = 10, height = 3)
        self.nameWidget.pack()
        bindForWidget(self.tag(), self.nameWidget)

    def dnd_end(self, target,  event):
        pass

    def clickEvent(self, event):
        self.focus()
        dnd.dnd_start(self, event)


