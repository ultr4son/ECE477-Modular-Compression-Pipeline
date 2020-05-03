import cv2
import numpy as np 


#Define the class Dither
class Dither:
	def __init__(self, input):
		self.input = input

	greyscale = True
	indices = 3
	ditherVal = 64

	#Returns the size of the input file
	def getSize(self):
	 	return self.input.size

	#Returns the shape of the input file
	def getShape(self):
		return self.input.shape


	#Returns True if file is greyscale and updates greyscale value
	def IsGreyScale(self, greyscale):
		return True

	#Dither image with resolution according to ditherVal
	def ditherImage(self, ditherVal):
		blue_channel = self.input[:,:,0]
		A1 = blue_channel//ditherVal
		A2 = np.multiply(A1, ditherVal)
		rows = blue_channel.shape[0]
		cols = blue_channel.shape[1]
		new_img = np.zeros((rows, cols, 3), np.uint8)
		new_img[:,:,0] = A2
		new_img[:,:,1] = A2
		new_img[:,:,2] = A2
		cv2.imwrite("dither_image999.jpg", new_img)





# Testing
img = cv2.imread('lena_grayscale.jfif')	#Input into this block

x = Dither(img)	#Creates an instance of the class Dither and assigns it to x
print (x.getSize())
print (x.getShape())

x.ditherImage(64)
