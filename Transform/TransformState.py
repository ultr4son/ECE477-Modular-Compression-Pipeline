import numpy as np


class State:
    """
        State to be carried through each transform.
    """
    def __init__(self, value):
        self.__value = value

    __value: object
    '''
        State value.
    '''
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newValue):

        #preserve shape and type information of bitmap if value is being changed from a bitmap to something else
        if isinstance(self.__value, np.ndarray) and not isinstance(newValue, np.ndarray):
            self.shape = self.__value.shape
            self.dtype = self.__value.dtype

        self.__value = newValue

    '''
        Statistics from previous operation
    '''
    statistics: dict

    '''
        Name of last compression used on value, so that the appropriate decompressor can be used.
    '''
    compression_type: str

    '''
        Shape of value the last time it was a numpy ndarray (a bitmap). Use this to reconstruct value back into a ndarray.
        Don't write to this.
    '''
    shape: tuple

    '''
        Type of each value in the numpy ndarray (a bitmap) last time value was a ndarary. Use this to reconstruct value back into a ndarray
        Don't write to this.
    '''
    dtype: np.dtype



