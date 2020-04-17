from Transform.TransformState import State
import numpy as np
import cv2 as cv
from Transform.TransformSystem import runTransformations

class ThompsonImageCompression:
    """
    This is a cool new compression algorithm made by me
    """

    def __init__(self, divideBy = 1):
        #An extra parameter that will be given to the class when instantiated
        self.divideBy = divideBy

    #This is what the transformation the class will do to the state value.
    #Keep this function the same name and format across all transformation classes so the system knows what to call!
    def transform(self, state: State):

        #Value assumed to be a numpy matrix
        value: np.ndarray = state.getValue()

        #Get initial size  for statistics
        initialSizeBytes = value.size * value.itemsize

        #Start compression algorithm
        #Construct what rows to keep in array
        keep = []
        for i in range(value.shape[0]):
            keep.append(i % self.divideBy == 0)

        #Remove rows that are false in keep
        value = np.compress(keep, value, axis=0)

        #Get final size for statistics
        finalSizeBytes = value.size * value.itemsize

        #Store modified value
        state.setValue(value)

        #Add statistics
        #Statistics list should only contain values from this transformation (Don't use append(), make a new list)
        state.statistics = ["Initial Size: " + str(initialSizeBytes), "Final Size: " + str(finalSizeBytes)]

        return state

#Main
if __name__ == "__main__":

    #Get test image
    initialValue = cv.imread("burmese.jpg")

    (final, record) = runTransformations([ThompsonImageCompression(3).transform, ThompsonImageCompression(2).transform], initialValue)

    cv.imshow("Initial", initialValue)

    #Show results to user
    i = 0
    for state in record:
        cv.imshow("State " + str(i), state.getValue())
        print("Statistics for transform " + str(i))
        for stat in state.statistics:
            print(stat)

        i = i + 1

    cv.waitKey(0)  # waits until a key is pressed
    cv.destroyAllWindows()  # destroys the window showing image





