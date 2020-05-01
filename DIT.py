import cv2
import numpy as np 


#Define the class Dither
class Dither:
	def __init__(self, input):
		self.input = input

	greyscale = True
	indices = 3
	ditherVal = 64
	pixelVal = 4
	ditheredImageArray = ""

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
	def ditherGreyscaleImage(self, ditherVal, outputFileName):
		blue_channel = self.input[:,:,0]
		A1 = blue_channel//ditherVal
		A2 = np.multiply(A1, ditherVal)
		rows = blue_channel.shape[0]
		cols = blue_channel.shape[1]
		new_img = np.zeros((rows, cols, 3), np.uint8)
		new_img[:,:,0] = A2
		new_img[:,:,1] = A2
		new_img[:,:,2] = A2
		self.ditherImageArray = A1
		cv2.imwrite(outputFileName, new_img)
		self.pixelVal = (255//ditherVal)
		#testing
		#print(blue_channel)
		#print(A1)	#A1 has pixel values before encoding
		#print(A2)	#A2 has pixel values after encoding

	#Dither a color image
	def ditherRGBimage(self, ditherVal, outputFileName):
		B_chan = self.input[:,:,0]
		R_chan = self.input[:,:,2]
		G_chan = self.input[:,:,1]
		
		AB1 = B_chan//ditherVal
		AB2 = np.multiply(AB1,ditherVal)

		AR1 = R_chan//ditherVal
		AR2 = np.multiply(AR1,ditherVal)

		AG1 = G_chan//ditherVal
		AG2 = np.multiply(AG1,ditherVal)

		rows = B_chan.shape[0]
		cols = B_chan.shape[1]

		new_img = np.zeros((rows,cols,3), np.uint8)
		new_img[:,:,0] = AB2
		new_img[:,:,2] = AR2
		new_img[:,:,1] = AG2
		self.ditherImageArray = AB1
		cv2.imwrite(outputFileName, new_img)
		self.pixelVal = (255//ditherVal)	


		

	#Encode the dithered image
	def encode(self):
		encoded_file = self.ditherImageArray
		print(encoded_file)
		print(encoded_file.size)




# Testing
img = cv2.imread('aa_cat.jpg')	#Input into this block
x = Dither(img)	#Creates an instance of the class Dither and assigns it to x
print("Size of input file (in Bytes): ", x.getSize())
print("Shape of input file (rows, columns, dimensions per pixel): ",x.getShape())
#Dither image according to a factorable input
#and output to file name
x.ditherRGBimage(64, "dither_image985.jpg")
#New pixel value range
print("Value range of pixels of new image: 0 to", x.pixelVal)

