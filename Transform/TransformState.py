
class State:
    """
        State to be carried through each transform.
    """
    def __init__(self, value):
        self.__value = value

        self.statistics = []

    __value: object
    '''
        State value.
    '''
    def getValue(self):
        return self.__value


    def setValue(self, newValue):

        self.__value = newValue

    '''
        Statistics from previous operation
    '''
    statistics: list

    name:str
    tree: object

