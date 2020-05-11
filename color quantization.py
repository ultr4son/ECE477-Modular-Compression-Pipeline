import numpy as np
import cv2
from PIL import Image
import PIL
import matplotlib.pyplot as plt

class Color_Quantizaion:
    def __init__(self, input):
        self.input = input

    ## Use Pillow to quantizatize without K means
    def random_quantization(self):
        # quantize a image
        rimg = self.input.quantize(16)
        # to show specified image
        rimg.show()
        return

    ## Use Opencv to quantizatize with K means
    def kmeans_quantization(self):
        Z = self.input.reshape((-1, 3))
        # convert to np.float32
        Z = np.float32(Z)
        # define criteria, number of clusters(K) and apply kmeans()
        i = 0
        k_list = [2, 4, 8, 16, 32]
        # title_list = [Kmean=2    16KB,Kmean=4    21KB,Kmean=8    23KB,Kmean=16   24KB]
        imgname_list = ['k2', 'k4', 'k8', 'k16', 'k32']
        for K in k_list:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            # Now convert back into uint8, and make original image
            center = np.uint8(center)
            res = center[label.flatten()]
            imgname_list[i] = res.reshape((self.input.shape))
            i += 1
        cv2.imshow('Kmean=2    135KB', imgname_list[0])
        cv2.imshow('Kmean=4    170KB', imgname_list[1])
        cv2.imshow('Kmean=8    191KB', imgname_list[2])
        cv2.imshow('Kmean=16    194KB', imgname_list[3])
        cv2.imshow('Kmean=32    198KB', imgname_list[4])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

##test
img = Image.open('LenaBaboon.jpg')
image = Color_Quantizaion(img)
image.random_quantization()

img = cv2.imread('LenaBaboon.jpg')
cv2.imshow('Original    774KB',img)
image = Color_Quantizaion(img)
image.kmeans_quantization()





