import os
import cv2

class Jpeg:
    def __init__(self, input):
        self.input = input
        return

    #Quality range is 0 to 95
    def encode(self, img, output_file, quality):
        cv2.imwrite(output_file, img, [cv2.IMWRITE_JPEG_QUALITY, quality])    
        return os.path.getsize(output_file)

    def decode(self, input_file, output_file):
        cv2.imwrite(output_file, img)
        return os.path.getsize(output_file)

if __name__ == '__main__':    
    #Testing Jpeg class
    img = cv2.imread('MARBLES.BMP')
    transform = Jpeg(img)
    print(transform.encode(img, "MARBLES.jpg", 50))
    img = cv2.imread("MARBLES.jpg")
    print(transform.decode(img, "MARBLES2.BMP"))
