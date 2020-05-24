from queue import PriorityQueue
from Transform.TransformState import State

#Function used in encoding to sort indices
def column(matrix, i):
    return [row[i] for row in matrix]

class ARI:
    def __init__(self):
        return
        
    def encode(self, stateOb):
        in_string = stateOb.getValue()
        self.freq_dict = self.calculate_frequency(in_string)
        #Makes self.ranges list of lists
        self.make_ranges()
        interval = self.get_interval(in_string)
        final_string = self.range_to_bin_string(interval[0], interval[1])
        stateOb.statistics = ["Initial Binary String: "+str(stateOb.getValue()), "Encoded String: "+str(final_string), "Initial Size(Bytes): " + str(len(stateOb.getValue())*8), "Final Size(Bytes): " + str(len(final_string)/8)]
        stateOb.setValue(final_string)
        stateOb.name = "Arithmetic Encoding"
        return stateOb

    def decode(self, stateOb, freqs):
        """in_string = stateOb.getValue()
        code_value = self.bin_to_decimal(in_string)
        self.freq_dict = freqs
        print(self.freq_dict)

        
        self.make_ranges()
        print(self.freq_dict)
        #print(self.freq_dict)
        
        #self.freq_dict = freqs
        #print(freqs)"""

    def calculate_frequency(self, in_string):
        frequencies = dict()
        #Puts frequencies in a dictionary structure
        self.in_string_length = 0
        for ch in in_string:
            self.in_string_length += 1
            if ch in frequencies.keys():
                frequencies[ch] += 1
            else:
                frequencies[ch] = 1 
        return frequencies

    def make_ranges(self):
        
        ordered_freqs = PriorityQueue()
        for ch, freq in self.freq_dict.items():
            self.freq_dict[ch] = self.freq_dict[ch]/self.in_string_length
            ordered_freqs.put((freq/self.in_string_length, ch))
        #Creating a list of lists in the form of [[char1, lower range1, higher range1], [char2, lower range...]...]
        self.ranges = list()
        #self.ranges.clear()
        prev_freq = ordered_freqs.get()
        self.ranges.append([prev_freq[1], 0, prev_freq[0]])
        i = 0
        while ordered_freqs.qsize() > 0:
            print(prev_freq)
            current_freq = ordered_freqs.get()
            self.ranges.append([current_freq[1], self.ranges[i][2], current_freq[0] + self.ranges[i][2]])
            prev_freqs = current_freq
            i += 1
        return
    
    
    def get_interval(self, in_string):
        high = 1.0
        low = 0.0
        rang = high - low
        k = 0
        for i in in_string:
            for j in self.ranges:
                if i == j[0]:
                    high = low + rang*j[2]
                    low = low + rang*j[1]
                    rang = high - low
        return [low, high]             

    def bin_to_decimal(self, bin_str):
        #turns the binary string into a decimal number
        decimal_num = 0.0
        for i in range(len(bin_str)):
            if int(bin_str[i]) == 1:
                decimal_num += pow(.5, i+1)
        return decimal_num

    def range_to_bin_string(self, low, high):
        code = list()
        while self.bin_to_decimal(code) < low or len(code) == 0:
            code.append(1)
            if self.bin_to_decimal(code) > high:        
                code.pop()
                code.append(0)
        final_string = ''.join([str(elem) for elem in code])
        #Returns the frequency values so decoder can parse binary string"""
        return final_string


if __name__ == "__main__":
        #Testing
        a = ARI()
        s = State("baac")
        s = a.encode(s)
        print(s.statistics)
        #a.decode(s, a.freq_dict)
