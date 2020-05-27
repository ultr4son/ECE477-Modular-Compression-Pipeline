from queue import PriorityQueue
from Transform.TransformState import State

class  Huffman_Node(object):
    def __init__(self, left = None, right = None):
        self.left = left
        self.right = right

class Huffman:
    def __init__(self):
        return
    
    def encode(self, stateOb):
        #Returns binary string that represent values
        in_string = stateOb.getValue()
        self.freq_dict = self.calculate_frequency(in_string)
        self.tree = self.make_tree(self.freq_dict)
        self.lookup_table = self.make_table(self.tree, list(), dict())       
        out_string  = list()
        for i in in_string:
            for j in self.lookup_table[i]:
                out_string.append(j)
        final_string = ''.join([str(elem) for elem in out_string]) 
        stateOb.statistics = ["Initial String: "+str(stateOb.getValue()), "Encoded String: "+str(final_string), "Initial Size(Bytes): " + str(len(in_string)), "Final Size(Bytes): " + str(len(final_string) / 8)]
        stateOb.setValue(final_string)
        stateOb.name = "Huffman Encode"
        stateOb.freq_table = self.freq_dict
        return stateOb

    def calculate_frequency(self, in_string):
        frequencies = dict()
        #Puts frequencies in a dictionary structure so they can be put into a tree
        for ch in in_string:
            if ch in frequencies.keys():
                frequencies[ch] += 1
            else:
                frequencies[ch] = 1 
        return frequencies

    #Makes a tree of nodes, where each node is a tuple (frequency, character, Huffman object)
    #Did this so I could use Priority Queue, because when calling put() queue must be able to
    #compare values and wouldn't be able to compare a Huffman tree
    def make_tree(self, frequencies):
        Q = PriorityQueue()
        for char, freq in frequencies.items():
            Q.put((freq, char, Huffman_Node()))
        while Q.qsize() > 1:
            node = Huffman_Node()
            node.left = Q.get()
            node.right = Q.get()
            frequency = node.left[0] + node.right[0]
            #assigned character to left node character, however could've been either, just
            #needed a valid value for it to compare to in case frequency values were the same
            z = (frequency, node.left[1], node)
            Q.put(z)
        return Q.get()
    
    def make_table(self, tree, code, table):
        #base case
        if tree[2].left == None and tree[2].left == None:
            table[tree[1]] = code
            return table
        
        #Have to concatenate instead of append so that code string
        #variable isn't changed for both rtable and ltable call
        ltable = self.make_table(tree[2].left, code + [1], table)
        rtable = self.make_table(tree[2].right, code + [0], table)
        ltable.update(rtable)
        return ltable

    def decode(self, stateOb):
        in_string = stateOb.getValue()
        lengthInitial = len(in_string)
        self.tree = self.make_tree(stateOb.freq_table)
        in_list = list()
        self.out_list = list()
        #Need to turn binary string into list first
        for i in in_string:
            in_list.append(i)
        self.decode_list(in_list, self.tree)
        #Turn list of chars back into a string
        final_string = ''.join([str(elem) for elem in self.out_list])
        stateOb.statistics = ["Initial Binary String: "+str(stateOb.getValue()), "Encoded String: "+str(final_string), "Initial Size(Bytes): " + str(len(in_string)/8), "Final Size(Bytes): " + str(len(final_string))]
        stateOb.setValue(final_string)
        stateOb.name = "Huffman Decode"
        return stateOb


    def decode_list(self, in_list, tree):
        if tree[2].left == None and tree[2].right == None:
            #Adds character to list
            self.out_list.append(tree[1])
            #if string isn't empty add the next character
            if in_list:
                self.decode_list(in_list, self.tree)
        else:
            temp = int(in_list.pop(0))

            if temp == 1:
                self.decode_list(in_list, tree[2].left)
            elif temp == 0:
                self.decode_list(in_list, tree[2].right)

if __name__ == '__main__':
    #in_string = "Hello World this is everett the quick brown fox jumped over the lazy dog"
    huf = Huffman()
    s = State("aaabcccd")
    print("Input String:  \t", s.getValue())
    
    s = huf.encode(s)
    print("Encoded String:\t", s.getValue())
    print("Lookup Table:  \t", s.freq_table)
    for stat in s.statistics:
        print(stat)

    huf.decode(s)
    print("Decoded String:\t", s.getValue())

    for stat in s.statistics:
        print(stat)
