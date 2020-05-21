import numpy as np

class BitmapToBytes:
    def encode(self, stateOb):
        stateOb.name = "Bitmap To Bytes"
        stateOb.setValue(stateOb.getValue().tostring())
        return stateOb

class BytesToBitmap:
    def __init__(self, aspect = 4/3):
        self.aspect = aspect

    def encode(self, stateOb):
        value = stateOb.getValue()
        asList = list(value)
        xLength = int(len(asList) * self.aspect)
        yLength = int(len(asList) * (1/self.aspect))
        arr = np.frombuffer(value)
        arr.reshape((xLength, yLength))
        stateOb.setValue(arr)
        return stateOb