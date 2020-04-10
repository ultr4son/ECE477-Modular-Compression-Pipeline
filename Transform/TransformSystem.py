"""
Defines system for running transformations.
Primary interface is the function runTransformations.
"""
from pymonad import State, unit, curry
import numpy as np
import copy
from Transform.TransformState import State as TState
import Transform.Transforms as Transforms

def runTransformations(transforms, initialState):
    """
    Call this function with the user's selected transforms.
    transforms: a list of functions that take an input value of type State and return an output value of type State. Expects that State.value is of the appropriate type for each function.
    initialState: the initial State value.
    returns: (State, [State]), as in (The result of the final operation, [The result of each operation in series])
    """

    system = TransformSystem(initialState)

    system.addTransforms(transforms)

    return system.runSystem()


# @curry splits each parameter such that a new function with the parameter applied is returned, such that a call to record(transform, value) becomes record(transform)(value)
# This allows for simple partial application of a function
@curry
def record(transform, value):
    """
        Wrap transform so that its results are recorded
    """

    @State
    def record_state(prevRecord):
        result = transform(value)
        prevRecord.append(copy.deepcopy(result))
        return (result, prevRecord)

    return record_state


class TransformSystem:
    __transform: State

    def __init__(self, initialState):
        """
        Create a transform system with the initial state initialState
        """

        # Set initial transform to just output initialState
        self.__transform = unit(State, initialState)

    def addTransform(self, transform):
        """
        Append a transform to the system.
        Transform is a function that takes a value, modifies it, and returns the modified version, in the format (s)->s'
        """

        # Link the output of __transform to transform using >>
        self.__transform = self.__transform >> record(transform)

    def addTransforms(self, transforms):
        """
        Append many transforms to the system, applied left to right.
        """
        for t in transforms:
            self.addTransform(t)

    def runSystem(self):
        """
        Run the system and return the result.
        Returns: (S, [S]), as in (The output of the last transform, a record of outputs from each transform in the system)
        """
        # Run the transform with the inital state of []
        return self.__transform([])


if __name__ == "__main__":
    initialState = TState(np.array([
        [1,1,1],
        [1,0,1],
        [1,0,0]
    ]))

    system = TransformSystem(initialState)

    system.addTransforms([Transforms.imageToBytes, Transforms.imageBytesToImage])

    result = system.runSystem()

    print(result[0].value)

    #Extract value from state
    print(list(map(lambda r: r.value, result[1])))
