import numpy as np
import math

class BitmapToBytes:
    def encode(self, stateOb):
        stateOb.name = "Bitmap To Bytes"
        bytes = stateOb.getValue().tobytes()
        asString = "".join(map(chr, bytes))
        stateOb.setValue(asString)
        return stateOb

class BytesToBitmap:
    def __init__(self, aspect = 4/3):
        self.aspect = aspect

    def encode(self, stateOb):
        value = stateOb.getValue()
        ords = list(map(ord, value))
        arr = np.frombuffer(bytearray(ords), dtype=np.uint8)
        xLength = int(math.sqrt((arr.size / 3) * self.aspect))
        yLength = int(math.sqrt((arr.size / 3) * 1/self.aspect))
        arr = np.resize(arr, xLength * yLength * 3)
        arr = arr.reshape((xLength, yLength, 3))
        stateOb.setValue(arr)
        stateOb.name = "Bytes To Bitmap"
        return stateOb