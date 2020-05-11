import numpy as np
import cv2
from PIL import Image
import PIL
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Color_Space:
    def __init__(self, input):
        self.input = input

    ##Gray
    def Gray(self):
        gray_img = cv2.cvtColor(self.input, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale image', gray_img)
        #cv2.imwrite('gray.jpg', gray_img)
        cv2.waitKey()
        return

    ##RGB
    def RGB(self):
        B, G, R = cv2.split(self.input)  # separate BGR
        zeros = np.zeros(self.input.shape[:2], dtype="uint8")  # build a matrix whose size is same as image
        b = cv2.merge([B, zeros, zeros])  # build B image
        g = cv2.merge([zeros, G, zeros])  # build G image
        r = cv2.merge([zeros, zeros, R])  # build R image
        rgb_merge = cv2.merge([B, G, R])  # combine RGB
        rgb = np.vstack([rgb_merge, r, g, b])
        cv2.imshow('RGB image', rgb)
        #cv2.imwrite('RGB.jpg', rgb)
        cv2.waitKey()
        return

    ##YUV
    def YUV(self):
        def make_lut_u():
            return np.array([[[i,255-i,0] for i in range(256)]],dtype=np.uint8)
        def make_lut_v():
            return np.array([[[0,255-i,i] for i in range(256)]],dtype=np.uint8)

        yuv_img = cv2.cvtColor(self.input, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(yuv_img)

        lut_u, lut_v = make_lut_u(), make_lut_v()

        # Convert back to BGR so we can apply the LUT and stack the images
        y = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
        u = cv2.cvtColor(u, cv2.COLOR_GRAY2BGR)
        v = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)

        u_mapped = cv2.LUT(u, lut_u)
        v_mapped = cv2.LUT(v, lut_v)

        yuv = np.vstack([self.input, y, u_mapped, v_mapped])
        cv2.imshow('YUV image', yuv)
        #cv2.imwrite('YUV.jpg', yuv)
        cv2.waitKey()
        return

##test
img = cv2.imread('test.png')
image = Color_Space(img)
image.Gray()
image.RGB()
image.YUV()
