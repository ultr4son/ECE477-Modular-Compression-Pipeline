import numpy as np
import cv2
from PIL import Image
import os
from Transform.TransformState import State


class Color_Quantizaion:
    def __init__(self, input):
        self.input = input

    """
    ## Use Pillow to quantizatize without K means
    def random_quantization(self, State):
        K = input('Number of color quantization:')
        K = int(K)
        # quantize a image
        rimg = self.input.quantize(8)
        rimg.save("randomQ.png")
        # to show specified image
        rimg.show()
        initialsize = os.path.getsize('LenaBaboon.jpg')
        randomQsize = os.path.getsize('randomQ.png')
        State.statistics = ["Initial Size: " + str(initialsize), "Random Quantization Size: " + str(randomQsize)]
        State.name = "Random Color Quantization"
        #print(State.statistics)
        return State

    """

    ## Use Opencv to quantizatize with K means
    def kmeans_quantization(self, State):
        K = input('Number of color quantization:')
        K = int(K)
        Z = self.input.reshape((-1, 3))
        # convert to np.float32
        Z = np.float32(Z)
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        KmeansQ = res.reshape((self.input.shape))
        # cv2.imwrite('original.jpg', img)
        # cv2.imwrite('kmeansQ.jpg', KmeansQ)
        # cv2.imshow('Kmeans', KmeansQ)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        initialsize = img.size * img.itemsize#os.path.getsize('original.jpg')
        kmeansQsize = img.size * img.itemsize #os.path.getsize('kmeansQ.jpg')
        State.setValue(KmeansQ)
        State.statistics = ["Initial Size: " + str(initialsize), "Kmeans Quantization Size: " + str(kmeansQsize), img]
        State.name = "Kmeans Color Quantization"
        return State


if __name__ == "__main__":
    ##test
    s = State("")
    """
    img = Image.open('LenaBaboon.jpg')
    State = Color_Quantizaion(img)
    Random_Quantization = State.random_quantization(img)
    for r in Random_Quantization.statistics:
        print(r)
    """
    img = cv2.imread('LenaBaboon.jpg')
    State= Color_Quantizaion(img)
    Kmeans_Quantization = State.kmeans_quantization(s)
    for i in Kmeans_Quantization.statistics:
        print(i)
