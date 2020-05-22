import cv2
import numpy
from tkinter import *
from Transform.TransformState import State
from LZW import LZW
from RLE import RLE
class Window(Frame):
    def outputFunc(self,stateObList,output):
        i=0
        j=0
        k=0
        viewButton=[]
        for stateOb in stateObList:
            #print(stateObList[i].getValue())
            #print(stateOb.getValue())

            viewButton.append(Button(self, text=stateOb.name,command=lambda stateOb=stateOb:self.outputInfo(stateOb,output)))#kept it as transform because formatting is a bit easier
            viewButton[i].place(x=j, y=k)
            #viewButton[i].pack(fill=BOTH,expand=1)
            i+=1
            j+=200
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
    def outputInfo(self,stateOb,output):
        #split = Tk()
        if self.counter>0:
            if isinstance(self.picName,str):
                cv2.destroyWindow(self.picName)
            for pics in self.picInfo:
                if isinstance(pics,str):
                    cv2.destroyWindow(pics)
            self.splitted.destroy()

        self.picInfo=[]
        split=Toplevel(output)
        self.splitted=split
        self.counter+=1
        """
        mainFrame = Frame(split)
        mainFrame.grid()
        entryFrame=Frame(mainFrame,width=400,height=200)
        entryFrame.grid(row=0,column=1)
        entryFrame.columnconfigure(0,weight=10)
        entryFrame.grid_propagate(False)
        """
        #split.geometry("400x200")
        #cv2.namedWindow('tk',cv2.WINDOW_NORMAL) no way to put text not on the photo
        #cv2.setWindowTitle("name")
        split.title(stateOb.name)#if i can get some info about the type of transform
        if isinstance(stateOb.getValue(),str):
            text = Label(split,text=stateOb.getValue())
            text.pack(fill=BOTH,padx=50,expand=1,side=TOP)
            #print(stateOb.getValue())
        else:
            self.picName=stateOb.name
            cv2.imshow(stateOb.name,stateOb.getValue())
            #self.picName="hello"
            #cv2.imshow("hello",stateOb.getValue())
            #print("do Imshow....")
        l=0
        for stat in stateOb.statistics:
            l+=1
            if isinstance(stat,str):
                text = Label(split,text=stat)
                text.pack(fill=BOTH,expand=1,padx=50,side=TOP)
            else:
                self.picInfo.append('tk'+str(l))
                cv2.imshow('tk'+str(l),stat)
            #print(stat)
        #split.destroy()
    def __init__(self, master=None,x=600,y=300):#can initilize with a window size the number of total transforms equal (x*y)/5000
        Frame.__init__(self, master)
        self.master = master
        self.x=x
        self.y=y
        self.counter=0
        self.picName=None
        self.picInfo=None
        self.init_window()
        #self.split=Tk()

    #Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Output")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        #self.master.geometry("")
        self.master.geometry(str(self.x)+"x"+str(self.y))

if __name__ == "__main__":
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
    outputOb.outputFunc([encodedL,encodedr1,encodedr2,encodedr3,s5,s6,s7,s8,s9,s10,s11],output)
    output.mainloop()
    #root.mainloop()
    #print("hello world")
    #cv2.namedWindow("Output",0)
    #cv2.waitKey(1)
    #cv2.createTrackbar('Transform1','Output',0,1,outputFunc)
