import tkinter as tk

class ParameterInput(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
    def setParameters(self, parameters, displayNames):
        row = 0
        for p in parameters.keys():
            displayLabel = tk.Label(self, text = displayNames[p])
            displayLabel.grid(column = 0, row = row)

            variable = tk.StringVar(self, parameters[p], p)
            tk.Entry(self, textvariable = variable, validate="focusout", validatecommand= self.handleSetVariable(p, variable))
            row = row + 1

    def getParameters(self):
        return self.parameters

    def handleSetVariable(self, p, variable):
        def callback():
            self.parameters[p] = variable.get()
        return callback