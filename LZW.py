#build a list from the start so if its "no means no" the dictionary becomes ["no","o"," ","m","e"it becomes [0,1,]
import string
import sys
import numpy as np
import math
from TransformState import State
class LZW:
    def __init__(self,bitsUsed=10):#the number of bits used will represent how many entries are in the dictionary+256 ascii defualt is 10 bits
        self.__bitsUsed = bitsUsed
    def encode(self,stateOb):
        sizeOfDict = 256
        finalArray=[]
        finalString=""
        i=1
        length = len(stateOb.getValue())
        dictionary = {chr(i): i for i in range(sizeOfDict)}#ascii table up to 256
        s = stateOb.getValue()[0]
        for c in stateOb.getValue()[1:]:
            #c = stateOb.getValue()[i]
            #i=i+1
            #print("hi")
            #for j in range(0,len(dictionary)):
            if (s+c) in dictionary:
                #print(s)
                s = s+c
                #break
            else:
                finalArray.append(dictionary[s])
                dictionary[(s+c)] = sizeOfDict
                sizeOfDict = sizeOfDict+1
                s = c
        finalArray.append(dictionary[s])
        for i in range(0,len(finalArray)):
            finalString=finalString+'{0:0{j}b}'.format(int(finalArray[i]),j=self.__bitsUsed)#convert everything to binary
            #finalString=finalString+'{0:08b}'.format(int(finalArray[i]))
        stateOb.statistics = ["Initial Size(Bytes): " + str(length), "Final Size(Bytes): " + str(len(finalString)/8),"Initial String: "+str(stateOb.getValue()),"Encoded String: "+str(''.join(map(str,finalArray)))]
        stateOb.setValue(finalString)
        #print(finalArray)
        return stateOb
    def decode(self,stateOb):
        sizeOfDict = 256
        finalArray=[]
        finalString=""
        length = len(stateOb.getValue())
        dictionary = {i: chr(i) for i in range(sizeOfDict)}#ascii table up to 256
        #print("dict value: ",dictionary[94])
        #print(dictionary)
        binaryString=""
        i=0
        hold = 0
        number = ""
        while i < length-1:#convert everything to a decimal list
            for i in range(hold,hold+self.__bitsUsed):
                number = number + stateOb.getValue()[i]
            number = int(number,2)
            hold = i+1
            finalArray.append(number)
            number =""
        #print("dict value: ",dictionary[1])
        s = "NIL"
        for k in finalArray:
            #print(k)
            if k in dictionary:
                entry = dictionary[int(k)]
            else:#exception handler checks in case the dictionary hasnt been filled in yet
                entry = s + s[0]
            finalString=finalString+str(entry)
            if s != "NIL":
                dictionary[sizeOfDict] = (s+entry[0])#update dictionary
                sizeOfDict = sizeOfDict+1
            s = entry
        #print(finalString)
        stateOb.statistics = ["Initial Size(Bytes): " + str(length/8), "Final Size(Bytes): " + str(len(finalString)),"Initial Binary String: "+str(stateOb.getValue())]
        stateOb.setValue(finalString)
        return stateOb



l = LZW()
s = State("^WED^WE^WEE^WEB^WET")
print("\nThis is where encoding starts\n")
encodedVal= l.encode(s)
print("encoded code: ",encodedVal.getValue())#somehow get the class state
for stat in encodedVal.statistics:
    print(stat)
print("\nThis is where decoding starts\n")
decodedVal= l.decode(encodedVal)
print("decoded code: ",decodedVal.getValue())#somehow get the class state
for stat in decodedVal.statistics:
    print(stat)
