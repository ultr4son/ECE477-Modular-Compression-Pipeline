import cv2
import numpy as np 


#Define the class Dither
class Dither:
	def __init__(self,  ditherVal = 64):
		self.greyscale = False
		self.ditherVal = ditherVal

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
	def ditherGreyscaleImage(self, ditherVal):
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
		#cv2.imwrite(outputFileName, new_img)
		#self.pixelVal = (255//ditherVal)
		return new_img
		#testing
		#print(blue_channel)
		#print(A1)	#A1 has pixel values before encoding
		#print(A2)	#A2 has pixel values after encoding

	#Dither a color image
	def ditherRGBimage(self, input, ditherVal):
		B_chan = input[:,:,0]
		R_chan = input[:,:,2]
		G_chan = input[:,:,1]
		
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
#		self.ditherImageArray = AB1
#		cv2.imwrite(outputFileName, new_img)
#		self.pixelVal = (255//ditherVal)
		return new_img

		

	#Encode the dithered image
	def encode(self, stateOb):
		#encoded_file = self.ditherImageArray

		value = stateOb.getValue()
		stateOb.name = "Dithering"
		initialSize = value.size * value.itemsize
		if self.greyscale:
			value = self.ditherGreyscaleImage(value, self.ditherVal)
			stateOb.setValue(value)
		else:
			value = self.ditherRGBimage(value, self.ditherVal)
			stateOb.setValue(value)
		stateOb.statistics = ["Pixel Range: " + str(255//self.ditherVal), "Initial Size: " + str(initialSize), "Final Size " + str(value.size * value.itemsize)]
		return stateOb
		#print(encoded_file)
		#print(encoded_file.size)



if __name__ == "__main__":
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

