import tkinter as tk

class ParameterInput(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.widgets = []
        # self.grid()
    def setParameters(self, parameters, displayNames):
        row = 0
        self.parameters = parameters

        for w in self.widgets:
            w.grid_forget()
            w.destroy()
        self.widgets = []

        for p in parameters.keys():
            displayLabel = tk.Label(self, text = displayNames[p])
            displayLabel.grid(column = 0, row = row)
            self.widgets.append(displayLabel)

            variable = tk.IntVar(self, parameters[p], p)
            variable.trace("w",self.handleSetVariable(p, variable))
            entry = tk.Entry(self, textvariable = variable)
            entry.grid(row = row, column = 1)
            self.widgets.append(entry)
            row = row + 1

    def getParameters(self):
        return self.parameters

    def handleSetVariable(self, p, variable):
        def callback(*args):
            try:
                self.parameters[p] = variable.get()
            except tk.TclError:
                pass
        return callback
