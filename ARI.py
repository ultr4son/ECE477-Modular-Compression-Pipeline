import string
import sys
import numpy as np
import math
from Transform.TransformState import State

#Function used in encoding to sort indices
def column(matrix, i):
    return [row[i] for row in matrix]

class ARI:
	def __init__(self, runType):
		self.__runType = runType


	dummyVal = 0

	def encode(self, stateOb):
		#Read in file
		arr0 = stateOb.getValue()
		numEntries = len(arr0)
		arr1 = sorted(stateOb.getValue())
		print("Sorted Input: ", arr1)		

		#Dictionary to hold input values and associated probabilities
		unique, counts = np.unique(arr1, return_counts=True)		
		inputMap = dict(zip(unique,counts))
		inputMap = {k: v / total for total in (sum(inputMap.values()),) for k, v in inputMap.items()}
		uniqueEntries = len(inputMap.keys())
		#print(inputMap)

		#Create structured array to hold all values with different datatypes at each index
		b = sorted(inputMap.items(), key=lambda x: x[1], reverse=True)
		b2 = column(b, 0)
		b3 = column(b, 1)
		y1 = np.array(list(b2))					#Entry
		y2 = np.array(list(b3))					#Probability
		y3 = np.zeros(uniqueEntries)			#upperBound
		y4 = np.zeros(uniqueEntries)			#lowerBound
		records = np.rec.fromarrays((y1,y2,y3,y4), names=('entry','probability','uBound','lBound'))
		#print("Structured array of values and data types: \n", records, "\n", records.dtype)
		#print("Sum of all probabilities        : ", np.sum(records.probability[:])) 

		#Determine uBound and lBound
		#uBound
		dec = 1.0
		for i in range(0, len(records)):
			if i == 0:
				records.uBound[i] = dec
			else:
				dec = dec - records.probability[i-1]
				records.uBound[i] = dec
		#lBound
		for i in range(0, len(records)):
			if i == (len(records)-1):
				records.lBound[i] = 0.0
			else:
				records.lBound[i] = records.uBound[i+1]
		print("Array: ", records)

		#Determine interval value from list of entries
		interval = [0,0]
		print(arr0)
		for i in range(0, numEntries):			#i iterates through the input list
			#Get character from what is entered and the index of character in records
			char = arr0[i]		
			#Find character index
			for j in range(0,len(records.entry)):
				if char == records.entry[j]:
					charIndex = j

			if(i == 0):
				print("---------------")
				interval[0] = records.lBound[charIndex]
				interval[1] = records.uBound[charIndex]
				intervalRange = records.uBound[charIndex] - records.lBound[charIndex]
				
				#1. Calculate new probabilities
				for x in range(0, len(records)):
					records.probability[x] = records.probability[x] * records.probability[charIndex]

				#2. Calculate new upper bound for each entry in records
				dec = intervalRange
				for x in range(0, len(records)):
					if x == 0:
						records.uBound[x] = dec
					else:
						dec = dec - records.probability[x-1]
						records.uBound[x] = dec
				#3. Calculate new lower bound for each entry in records
				for x in range(0, len(records)):
					if x == (len(records)-1):
						records.lBound[x] = 0.0
					else:
						records.lBound[x] = records.uBound[x+1]


			else:
				intervalRange = intervalRange * records.probability[charIndex]
				interval[0] = records.lBound[charIndex]
				interval[1] = records.uBound[charIndex]
				intervalRange = records.uBound[charIndex] - records.lBound[charIndex]
				
				#1. Calculate new probabilities
				for x in range(0, len(records)):
					records.probability[x] = records.probability[x] * records.probability[charIndex]

				#2. Calculate new upper bound for each entry in records
				dec = intervalRange
				for x in range(0, len(records)):
					if x == 0:
						records.uBound[x] = dec
					else:
						dec = dec - records.probability[x-1]
						records.uBound[x] = dec
				#3. Calculate new lower bound for each entry in records
				for x in range(0, len(records)):
					if x == (len(records)-1):
						records.lBound[x] = 0.0
					else:
						records.lBound[x] = records.uBound[x+1]


			print("Iteration: ", i+1, " interval is: ", interval)
			print("Interval Range: ", intervalRange)
			print("Character: ", char)
			print("Character Index: ", charIndex)
			print("---------------")


			#Find smallest binary representation in interval variable
			print(interval[0].dtype)
			#print(len(interval[0]]))
			low = interval[0].astype(np.int64)
			print(low)
			print(low.dtype)
			#f1 = np.binary_repr(interval[0])
			#print(f1)



	def decode(self, stateOb):
		self.dummyVal = 2



if __name__ == "__main__":
	#Testing
	a = ARI(1)
	#s = State("AABCAACC")
	s = State("MMMMFFVVVF")
	#s = State("ABC")
	a.encode(s)
