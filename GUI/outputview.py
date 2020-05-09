import cv2
import numpy
from tkinter import *
from TransformState import State
from LZW import LZW
from RLE import RLE
class Window(Frame):
    def outputFunc(self,stateObList):
        i=0
        j=0
        k=0
        viewButton=[]
        for stateOb in stateObList:
            #print(stateObList[i].getValue())
            #print(stateOb.getValue())
            viewButton.append(Button(self, text="Transform"+str(i+1),command=lambda stateOb=stateOb:self.outputInfo(stateOb)))#kept it as transform because formatting is a bit easier
            viewButton[i].place(x=j, y=k)
            i+=1
            j+=100
            if j%self.x == 0:
                k+=50
                j=0
        #for stateOb in stateObList:
        #    viewButton = Button(self, text="Transform"+str(i),command=lambda:self.outputInfo(stateOb))
        #    viewButton.place(x=j, y=i)
        #    i+=1
        #    j+=100
        #text = Label(self,text=stateOb)
        #text.pack()
    def outputInfo(self,stateOb):
        split = Tk()
        #cv2.namedWindow('tk',cv2.WINDOW_NORMAL) no way to put text not on the photo
        #cv2.setWindowTitle("name")
        split.title(stateOb.name)#if i can get some info about the type of transform
        if isinstance(stateOb.getValue(),str):
            text = Label(split,text=stateOb.getValue())
            text.pack()
            #print(stateOb.getValue())
        else:
            cv2.imshow(stateOb.name,stateOb.getValue())
            #print("do Imshow....")
        l=0
        for stat in stateOb.statistics:
            l+=1
            if isinstance(stateOb.getValue(),str):
                text = Label(split,text=stat)
                text.pack()
            else:
                cv2.imshow('tk'+l,stat)
            #print(stat)
    def __init__(self, master=None,x=400,y=300):#can initilize with a window size the number of total transforms equal (x*y)/5000
        Frame.__init__(self, master)
        self.master = master
        self.x=x
        self.y=y
        self.init_window()


    #Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Output")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.master.geometry(str(self.x)+"x"+str(self.y))

output = Tk()

#size of the window
#output.geometry("400x300")
path=r'C:\Users\Ichen Lee\AppData\Local\Programs\Python\Python38-32\Scripts\yoda.jpeg'
imagej=cv2.imread(path,1)
#print(imagej)
#cv2.imshow('hello',imagej)
outputOb = Window(output)
s = State("qwAAAAAAAAAAAABBBBEEEJKAAAAA")
s1 = State("qwAAAAAAAAAAAABBBBEEEJKAAAAA")
s2= State("10000000000000010000000001110000000000000000000010000000000000000000000000000001100000000000")
s3 = State("^WED^WE^WEE^WEB^WET")
r1=RLE(0)
r2=RLE(1)
r3=RLE(2)
l=LZW()
encodedL=l.encode(s3)
encodedr1=r1.encode(s1)
encodedr2=r2.encode(s)
encodedr3=r3.encode(s2)
s4 = State("hello1")
s5= State("hi2")
s6 = State("bye3")
s7 = State("hello4")
s8= State("hi5")
s9 = State("bye6")
s10 = State("bye1")
s11=State(imagej)
outputOb.outputFunc([encodedL,encodedr1,encodedr2,encodedr3,s5,s6,s7,s8,s9,s10,s11])
output.mainloop()
#root.mainloop()
#print("hello world")
#cv2.namedWindow("Output",0)
#cv2.waitKey(1)
#cv2.createTrackbar('Transform1','Output',0,1,outputFunc)
