import string
import sys
import numpy as np
import math
from Transform.TransformState import State
class LZW:
    def __init__(self):#the number of bits used will represent how many entries are in the dictionary+256 ascii defualt is 10 bits
        self.__bitsUsed = 10
    def encode(self,stateOb):
        sizeOfDict = 256
        finalArray=[]
        finalString=""
        i=1
        length = len(stateOb.getValue())
        dictionary = {chr(i): i for i in range(sizeOfDict)}#ascii table up to 256
        s = stateOb.getValue()[0]
        for c in stateOb.getValue()[1:]:
            if (s+c) in dictionary: #if its in table, add together strings
                s = s+c
            else: #if not already in table, put int table
                finalArray.append(dictionary[s])
                dictionary[(s+c)] = sizeOfDict
                sizeOfDict = sizeOfDict+1
                s = c
        finalArray.append(dictionary[s])
        for i in range(0,len(finalArray)):
            finalString=finalString+'{0:0{j}b}'.format(int(finalArray[i]),j=self.__bitsUsed)#convert everything to binary
        stateOb.statistics = ["Initial Size(Bytes): " + str(length), "Final Size(Bytes): " + str(len(finalString)/8),"Initial String: "+str(stateOb.getValue()),"Encoded String: "+str(','.join(map(str,finalArray))),"Bits Used: "+str(self.__bitsUsed)]
        stateOb.setValue(finalString)
        stateOb.name="LZW Encode"
        return stateOb

    def decode(self,stateOb):
        sizeOfDict = 256
        finalArray=[]
        finalString=""
        length = len(stateOb.getValue())
        dictionary = {i: chr(i) for i in range(sizeOfDict)}#ascii table up to 256
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
        s = "NIL"
        for k in finalArray:
            if k in dictionary:
                entry = dictionary[int(k)]
            else:
                entry = s + s[0]
            finalString=finalString+str(entry)
            if s != "NIL":
                dictionary[sizeOfDict] = (s+entry[0])#update dictionary
                sizeOfDict = sizeOfDict+1
            s = entry
        stateOb.statistics = ["Initial Size(Bytes): " + str(length/8), "Final Size(Bytes): " + str(len(finalString)),"Initial Binary String: "+str(stateOb.getValue())]
        stateOb.setValue(finalString)
        stateOb.name="LZW Decode"
        return stateOb


if __name__ == "__main__":

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
