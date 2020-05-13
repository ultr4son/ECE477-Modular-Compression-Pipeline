from PIL import Image
import os
import numpy as np

from TransformState.py import State
from Transform.TransformSystem.py import runTransformations

class Jpeg:
    def __init__(self):

        return
    
    def encode(self, input_file, output_file, qual):
        img = Image.open(input_file)    
        img.save(output_file, "jpeg", quality = qual)
        return os.path.getsize(output_file)        

    def decode(self, input_file, output_file):
        img = Image.open(input_file)    
        img.save(output_file, "BMP")
        return os.path.getsize(output_file)


if __name__ == '__main__':    
    
    #Testing Jpeg class
    transform = Jpeg()
    print(transform.encode("MARBLES.BMP", "Marbles", 20))
    print(transform.decode("Marbles", "Marbles2"))
    
