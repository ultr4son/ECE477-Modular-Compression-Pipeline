import os
import cv2

class Jpeg:
    def __init__(self):
        return
    
    def update_img(self, input):
        self.input = input
        return

    #Quality range is 0 to 95
    def encode(self, output_file, quality):
        cv2.imwrite(output_file, self.input, [cv2.IMWRITE_JPEG_QUALITY, quality])    
        return os.path.getsize(output_file)

    def decode(self, output_file):
        cv2.imwrite(output_file, self.input)
        return os.path.getsize(output_file)

if __name__ == '__main__':    
    #Testing Jpeg class
    img = cv2.imread('MARBLES.BMP')
    transform = Jpeg(img)
    print(transform.encode("MARBLES.jpg", 10))
    img = cv2.imread("MARBLES.jpg")
    transform.update_img(img)
    print(transform.decode("MARBLES2.BMP"))
