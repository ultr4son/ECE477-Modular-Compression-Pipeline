import os
import cv2

class Jpeg:
    def __init__(self, quality = 95):
        self.quality = quality
    
    def update_img(self, input):
        self.input = input
        return

    #Quality range is 0 to 95
    def encode(self, stateOb):
        value = stateOb.getValue()
        initialSize = value.size * value.itemsize
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
        (result, image) = cv2.imencode(".jpg", stateOb.getValue(), encode_param)
        stateOb.setValue(image)
        stateOb.name = "JPEG Encoding"
        stateOb.statistics = ["Initial Size: " + str(initialSize), "Final Size: " + str(image.size * image.itemsize)]
        return stateOb

    def decode(self, stateOb):
        value = stateOb.getValue()
        initialSize = value.size * value.itemsize
        image = cv2.imdecode(stateOb.getValue(), -1)
        stateOb.setValue(image)
        stateOb.name = "JPEG Decoding"
        stateOb.statistics = ["Initial Size: " + str(initialSize), "Final Size: " + str(image.size * image.itemsize)]
        return stateOb

if __name__ == '__main__':

    #Testing Jpeg class
    img = cv2.imread('MARBLES.BMP')
    transform = Jpeg(img)
    print(transform.encode("MARBLES.jpg", 10))
    img = cv2.imread("MARBLES.jpg")
    transform.update_img(img)
    print(transform.decode("MARBLES2.BMP"))
