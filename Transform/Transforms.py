import numpy as np

'''
    Transformations
'''

def imageToBytes(s):
    """
        Convert a numpy ndarray to bytes
    """
    s.value = s.value.tobytes()
    return s

def imageBytesToImage(s):
    """
    Convert bytes from a image converted to bytes to an image
    Expects that the number of bytes and type representation is the same as from the original image
    """
    s.value = np.frombuffer(s.value, dtype = s.dtype)
    s.value = s.value.reshape(s.shape)
    return s