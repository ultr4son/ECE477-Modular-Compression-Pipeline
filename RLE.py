import sys
import numpy as np
import math
from Transform.TransformState import State
class RLE:
    def __init__(self, runType=2,bitsUsed=5):#will change to 0, 1, or 2 0 for literal run, 1 for fill run and 2 for binary run
        self.__runType = runType#binary RLE needs another input can default to just 4?
        self.__bitsUsed = bitsUsed
    def runType1(self):
        return self.__runType

    def runType(self,newRunType):
        self.__runType = newRunType

    def bitsUsed(self):
        return self.__runType

    def bitsUsed(self,newBits):
        self.__bitsUsed = newBits
    def encode(self,stateOb):
        #print(type(stateOb.value()))
        #print(stateOb.value())
        finalArray=""
        initialArray=str(stateOb.getValue())
        length = len(str(stateOb.getValue())) #length of a string
        lengthInitial=len(str(stateOb.getValue()))
        lengthHolder= 0
        indexAmount=0
        i=0
        numberHolder=0
        countNums=0
        #print("length of string ",length)
        #length = 0
        count = 1 #count the number of repeated characters
        j = 0 #cycle through the number of repeated
        if self.__runType == 0:
            #stateOb.info(length+1)
            #This is above the change of value because attaching the length should only be 1 byte but since I needed to keep it a string
            #The number takes up string bytes depending on how big the number is for example 100 is 1 + 1 + 1 = 3 bytes each each character but RLE is done so that the number is represented with 1 byte.
            finalArray = '{0:08b}'.format(int(length))
            finalArray=finalArray+''.join(format(ord(x), '08b') for x in stateOb.getValue())
            #stateOb.setValue(str(length)+stateOb.getValue())
            stateOb.statistics = ["Initial Size(Bytes): " + str(lengthInitial), "Final Size(Bytes): " + str(lengthInitial+1),"Initial String: "+str(stateOb.getValue()),"Encoded String: "+str(str(length)+stateOb.getValue())]
            stateOb.setValue(finalArray)
            stateOb.name="RLE Encode Literal Run"
            return stateOb
        elif self.__runType == 1:
            count = 129 #msb is a 1 if this if statement is accessed
            while i < length:
                j = i+1#make sure this doesnt equal length
                if j>=length:
                    break
                #print("i value: ",stateOb.value1()[i])
                #print("j value: ",stateOb.value1()[j])
                #print("value: ",stateOb.value1()," index: ",i)
                while stateOb.getValue()[i] == stateOb.getValue()[j]:#count the number of duplicates
                    #print("value of legnth: ",length)
                    #print("value of j: ",j)
                    if j+1>=length:#if it reaches the last index remove the last index and increment count and break out of hte loop
                        stateOb.setValue(stateOb.getValue()[:j])
                        count=count+1
                        break
                    stateOb.setValue(stateOb.getValue()[:j]+stateOb.getValue()[j+1:])#cut out the duplicate character
                    #j=j+1#might not be needed
                    count=count+1
                    if count >= 255:
                        break
                    length = len(str(stateOb.getValue()))
                lengthHolder = len(str(stateOb.getValue()))#can maybe just convert the line below to binary
                #stateOb.setValue((''.join(format(ord(x), '08b') for x in stateOb.getValue()[0:j-1]))+('{0:08b}'.format(int(count)))+(''.join(format(ord(x), '08b') for x in stateOb.getValue()[j-1:])))#add in the number in front of the repeating character
                #print(stateOb.getValue())
                finalArray = finalArray+('{0:08b}'.format(int(count)))+(''.join(format(ord(x), '08b') for x in stateOb.getValue()[j-1]))
                #print(finalArray)
                stateOb.setValue(stateOb.getValue()[0:j-1]+str(count)+stateOb.getValue()[j-1:])#add in the number in front of the repeating character
                countNums=countNums+1#this is added each time a number is added so the correct filesize can be displayed
                length = len(str(stateOb.getValue()))
                #print("indexamount: ",length,"-",lengthHolder)
                indexAmount = length - lengthHolder
                numberHolder = numberHolder+indexAmount#collects the number of slots the numbers take up s
                #print("indexamount: ", indexAmount)
                #if count != 1:
                i= i+indexAmount+1
                #else:
                    #i = i+1
                count=129
            length = len(str(stateOb.getValue()))
            #print (finalArray)
            stateOb.statistics = ["Initial Size(Bytes): " + str(lengthInitial), "Final Size(Bytes): " + str(int(len(finalArray)/8)),"Initial String: "+str(initialArray),"Encoded String: "+str(stateOb.getValue())]
            stateOb.setValue(finalArray)
            stateOb.name="RLE Encode Fill Run"
            #stateOb.info(length-numberHolder+countNums) #where do we put the information like size? +128 for the 1 in msb, - numberHolder to take away the bytes numbers are holding + to add in the correct bytes numbers are holding
            return stateOb
        else:
            countZs=0
            i=0
            n = 0
            finalArray=""
            initialBString=stateOb.getValue()
            #holderArray=""
            decimal = (2**self.__bitsUsed)-1
            checkIfDecimals=0
            #if stateOb.value1()[0]=='1':
            #    finalArray=('0'*self.__bitsUsed)
            while i < length:
                if stateOb.getValue()[i] == '0':
                    countZs=countZs+1
                if stateOb.getValue()[i] == '1' or i+1==length:
                    if countZs>decimal:
                        checkIfDecimals=float(countZs/decimal)
                        if checkIfDecimals%1 < .00001:
                            n=math.ceil(n)
                            n=int(n)
                            for j in range(0,n):
                                finalArray=finalArray+('1'*self.__bitsUsed)
                            finalArray=finalArray+('0'*self.__bitsUsed)
                            countZs=0
                        else:
                            n=math.ceil(checkIfDecimals)
                            n= int(n)
                            for j in range(0,n-1):
                                countZs=countZs-decimal
                                finalArray=finalArray+('1'*self.__bitsUsed)
                            finalArray=finalArray+'{0:0{j}b}'.format(countZs,j=self.__bitsUsed)
                            countZs=0
                    else:
                        finalArray=finalArray+'{0:0{j}b}'.format(countZs,j=self.__bitsUsed)
                        countZs = 0
                    #while stateOb.value1()[i+1] == '1'
                    #    i=i+1
                i=i+1
            binaryHolder=""
            readableString=""
            i=0
            while i < len(finalArray):
                binaryHolder=binaryHolder+finalArray[i]
                i+=1
                if len(binaryHolder) == self.__bitsUsed:
                    readableString=readableString+str(int(binaryHolder,2))+","
                    binaryHolder=""
            stateOb.setValue(finalArray)
            stateOb.statistics = ["Initial Size(Bytes): " + str(lengthInitial/8), "Final Size(Bytes): " + str(len(finalArray)/8),"Initial Binary String: "+str(initialBString),"Encoded String: "+str(readableString),"Bits Used: "+str(self.__bitsUsed)]
            stateOb.name="RLE Encode Binary Run"
            return stateOb

    def decode(self,stateOb):#need to work on this next
        finalArray=""
        numberCount=0
        checkIfNew = 0
        letter = ""
        length = len(str(stateOb.getValue())) #length of a string
        lengthInitial=len(str(stateOb.getValue()))
        if self.__runType == 0:
            i = 8
            hold=8
            while i < length-1:
                for i in range(hold,hold+8):
                    letter = letter + stateOb.getValue()[i]
                letter = int(letter,2)
                letter = chr(letter)
                finalArray=finalArray+letter
                letter = ""
                hold = i+1

            #for i in range(0,len(stateOb.getValue())):
            #    if  stateOb.getValue()[i] != '0' and stateOb.getValue()[i] != '1' and stateOb.getValue()[i] != '2' and stateOb.getValue()[i] != '3' and stateOb.getValue()[i] != '4' and stateOb.getValue()[i] != '5' and stateOb.getValue()[i] != '6' and stateOb.getValue()[i] != '7' and stateOb.getValue()[i] != '8' and stateOb.getValue()[i] != '9':
            #        finalArray = finalArray + stateOb.getValue()[i]
                    #checkIfNew = 0
            #    else:
            #        numberCount=numberCount+1
            stateOb.statistics = ["Initial Size(Bytes): " + str(int(lengthInitial/8)), "Final Size(Bytes): " + str(len(finalArray)),"Initial Binary String: ",stateOb.getValue()]
            stateOb.setValue(finalArray)
            stateOb.name="RLE Decode Literal Run"
            #stateOb.statistics = ["Initial Size(Bytes): " + str(lengthInitial-numberCount+1), "Final Size(Bytes): " + str(len(finalArray))]
            #stateOb.info(len(finalArray))
            return stateOb
        elif self.__runType == 1:
            number = ""
            letter = ""
            i=0
            hold = 0
            while i < length-1:
                for i in range(hold,hold+8):
                    number = number + stateOb.getValue()[i]
                number = int(number,2)-128
                hold = i+1
                for i in range(hold,hold+8):
                    letter = letter + stateOb.getValue()[i]
                letter = int(letter,2)
                letter = chr(letter)
                finalArray=finalArray+(str(str(letter)*int(number)))
                letter = ""
                number = ""
                hold = i+1
            #print("obtained value: ",stateOb.getValue())
            #while j < len(stateOb.getValue()):
            #    number = ""
            #    i=j
            #    jumps=0
            #    while stateOb.getValue()[i] == '0' or stateOb.getValue()[i] == '1' or stateOb.getValue()[i] == '2' or stateOb.getValue()[i] == '3' or stateOb.getValue()[i] == '4' or stateOb.getValue()[i] == '5' or stateOb.getValue()[i] == '6' or stateOb.getValue()[i] == '7' or stateOb.getValue()[i] == '8' or stateOb.getValue()[i] == '9':
            #        number=number+stateOb.getValue()[i]
            #        i=i+1
            #        jumps=jumps+1
            #        numberCount = numberCount+1
            #    if i!=j:
                    #print("number value: ",number,"i value: ",i)
            #        finalArray=finalArray+((int(number)-128)*stateOb.getValue()[i])
                #print("final array value: ",finalArray)
            #    j=j+jumps+1
            stateOb.statistics = ["Initial Size(Bytes): " + str(int(lengthInitial/8)), "Final Size(Bytes): " + str(len(finalArray)),"Initial Binary String: ",stateOb.getValue()]
            stateOb.setValue(finalArray)
            stateOb.name="RLE Decode Fill Run"
            #stateOb.statistics = ["Initial Size(Bytes): " + str((lengthInitial-numberCount)*2), "Final Size(Bytes): " + str(len(finalArray))]
            #stateOb.info(len(finalArray))
            return stateOb
        else:
            i=0
            hold=0
            checkIfOne = 1
            initialBString=stateOb.getValue()
            while hold < (len(stateOb.getValue())-1):
                arrayHold=""
                for i in range(hold,hold+self.__bitsUsed):
                    arrayHold=arrayHold+stateOb.getValue()[i]
                hold=i+1
                #print(i)
                if arrayHold == ('1'*self.__bitsUsed):
                    finalArray=finalArray+("0"*int(arrayHold,2))
                    checkIfOne = 0
                elif arrayHold == ('0'*self.__bitsUsed) and checkIfOne == 1:
                    finalArray=finalArray+"1"
                elif arrayHold == ('0'*self.__bitsUsed) and checkIfOne == 0:
                    checkIfOne=1
                    if hold!=len(stateOb.getValue()):
                        finalArray=finalArray+"1"
                else:
                    finalArray=finalArray+("0"*int(arrayHold,2))
                    if hold!=len(stateOb.getValue()):
                        finalArray=finalArray+"1"

            stateOb.setValue(finalArray)
            stateOb.statistics = ["Initial Size(Bytes): " + str(lengthInitial/8), "Final Size(Bytes): " + str(len(finalArray)/8),"Initial Binary String: "+str(initialBString)]
            stateOb.name="RLE Decode Binary Run"
            #stateOb.info(len(finalArray)/8)
            return stateOb


if __name__ == "__main__":
    #main
    r = RLE(2)
    #s = State("qwAAAAAAAAAAAABBBBEEEJKAAAAA")
    #s = State("1000100001")
    s = State("10000000000000010000000001110000000000000000000010000000000000000000000000000001100000000000")

    print("\nThis is where encoding starts\n")
    encodedVal= r.encode(s)
    #print(r.runType1())
    print("encoded code: ",encodedVal.getValue())#somehow get the class state
    for stat in encodedVal.statistics:
        print(stat)
    #print("size of encoded code(bytes): ",encodedVal.info1())#somehow get the class state
    decodedVal = r.decode(encodedVal)
    #print(r.runType1())
    print("\nThis is where decoding starts\n")

    print("decoded message: ",decodedVal.getValue())#somehow get the class state
    for stat in decodedVal.statistics:
        print(stat)
    #print("size of decoded message code(bytes): ",decodedVal.info1())#somehow get the class state
