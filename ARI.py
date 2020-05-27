from queue import PriorityQueue
from Transform.TransformState import State
from decimal import *

class ARI:
    def __init__(self):
        return
        
    def encode(self, stateOb):
        in_string = stateOb.getValue()
        self.freq_dict = self.calculate_frequency(in_string)
        #Makes self.ranges list of lists
        self.make_ranges()
        interval = self.get_interval(in_string)
        final_string = self.range_to_bin_string(Decimal(interval[0]), Decimal(interval[1]))
        stateOb.statistics = ["Initial String: "+str(stateOb.getValue()), "Encoded String: "+str(final_string), "Initial Size(Bytes): " + str(len(stateOb.getValue())), "Final Size(Bytes): " + str(len(final_string)/8)]
        stateOb.setValue(final_string)
        stateOb.name = "Arithmetic Encoding"
        stateOb.freq_dict = self.freq_dict
        stateOb.str_length = len(in_string)
        return stateOb

    def decode(self, stateOb):
        in_string = stateOb.getValue()
        code_value = self.bin_to_decimal(in_string)
        self.freq_dict = stateOb.freq_dict
        self.make_ranges()
        out_list = self.eval_interval(self.ranges, code_value, stateOb.str_length)
        final_string = ''.join([str(elem) for elem in out_list]) 
        stateOb.statistics = ["Encoded Binary String: "+str(stateOb.getValue()), "Decoded String: "+str(final_string), "Initial Size(Bytes): " + str(len(in_string)/8), "Final Size(Bytes): " + str(len(final_string))]
        stateOb.setValue(final_string)
        stateOb.name = "Arithmetic Decoding"
        return stateOb

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
        total_freqs = 0
        for ch, freq in self.freq_dict.items():
            total_freqs += freq
        ordered_freqs = PriorityQueue()
        for ch, freq in self.freq_dict.items():
            self.freq_dict[ch] = Decimal(self.freq_dict[ch])/Decimal(total_freqs)
            ordered_freqs.put((Decimal(freq)/Decimal(total_freqs), ch))
        #Creating a list of lists in the form of [[char1, lower range1, higher range1], [char2, lower range...]...]
        self.ranges = list()
        prev_freq = ordered_freqs.get()
        self.ranges.append([prev_freq[1], 0, Decimal(prev_freq[0])])
        i = 0
        while ordered_freqs.qsize() > 0:
            current_freq = ordered_freqs.get()
            self.ranges.append([current_freq[1], Decimal(self.ranges[i][2]), Decimal(current_freq[0]) + Decimal(self.ranges[i][2])])
            prev_freqs = current_freq
            i += 1
        return
    
    
    def get_interval(self, in_string):
        high = Decimal(1.0)
        low = Decimal(0.0)
        rang = Decimal(high) - Decimal(low)
        for i in in_string:
            for j in self.ranges:
                if i == j[0]:
                    high = Decimal(low) + rang*Decimal(j[2])
                    low = Decimal(low) + rang*Decimal(j[1])
                    rang = Decimal(high) - Decimal(low)
        return [low, high]             
        
    def eval_interval(self, ranges, value, str_length):
        output_string = list()
        while len(output_string) < str_length:
            check_once = False
            #check_once makes sure that it iterates only once into the if statement for every j value
            for i in range(len(ranges)):
                if ranges[i][1] <= Decimal(value) and ranges[i][2] > Decimal(value) and check_once == False:
                    low = Decimal(ranges[i][1])
                    high = Decimal(ranges[i][2])
                    rang = Decimal(high - low)
                    value = (Decimal(value)-Decimal(low))/Decimal(rang)
                    if value == 0:
                        output_string.append(ranges[i-1][0])
                    else:
                        output_string.append(ranges[i][0])
                    check_once = True
        return output_string

    def bin_to_decimal(self, bin_str):
        #turns the binary string into a decimal number
        decimal_num = Decimal(0.0)
        for i in range(len(bin_str)):
            if int(bin_str[i]) == 1:
                decimal_num += Decimal(pow(.5, i+1))
        return decimal_num

    def range_to_bin_string(self, low, high):
        code = list()
        while Decimal(self.bin_to_decimal(code)) < Decimal(low) or len(code) == 0:
            code.append(1)
            if Decimal(self.bin_to_decimal(code)) > Decimal(high):        
                code.pop()
                code.append(0)
        final_string = ''.join([str(elem) for elem in code])
        #Returns the frequency values so decoder can parse binary string"""
        return final_string


if __name__ == "__main__":
        #Testing
        a = ARI()
        s = State("aaaabbbbccccaaaabbbbccccaaaabbbbccccaaaabbbbccccabcd")
        s = a.encode(s)
        print(s.statistics)
        a.decode(s)
        print(s.statistics)
