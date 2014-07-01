import sys

class MessageDecoding(object):
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if expected == result:
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, message):
        return Decoder(message).decode()
    
    
class Decoder(object):
    def __init__(self, message):
        self.message = message
    
    def decode(self):
        header, message = self.get_header_and_message()
        translator = Translator(header)
        return translator.convert(message)
    
    def get_header_and_message(self):
        i = 0
        while i < len(self.message):
            char = self.message[i]
            if char in ('0', '1'):
                header = self.message[:i]
                message = self.message[i:]
                return header, message
            i += 1
        
        assert False, "Couldn't find the binary message..."
    
    
def binary_string_to_int(num):
    i = len(num) - 1
    value = 0
    while i >= 0:
        value += int(num[i]) * (2 ** (len(num) - 1 - i))
        i -= 1
    return value

def is_all_ones(number):
    n = str(number)
    for char in n:
        if char != '1':
            return False
    return True

def int_to_binary_string(num):
    string = bin(num).replace("0b", "")
    return string

class Translator(object):
    def __init__(self, header):
        self.header = header
        self.map = {}
        
        self.init_translation_mapping()
    
    def init_translation_mapping(self):
        counter = BinaryCounter()
        
        for char in self.header:
            self.map[counter.key()] = char
            counter.next()
    
    def convert(self, message):
        # First three digits represents the number of digits in each character key.
        num_digits_str = message[:3]
        num_digits = binary_string_to_int(num_digits_str)
        translated = ""

        i = 3
        key = message[i:i+num_digits]
        while not is_all_ones(key) and i < len(message) - 3:
            key = message[i:i+num_digits]
            
            if is_all_ones(key):
                # Remove the string of ones and start the conversion over for the remaining string.
                i += num_digits
                break
            
            char = self.map[key]
            
            translated += char
            i += num_digits
        
        remainder = message[i:]
        if remainder == '000':
            return translated
        else:
            return translated + self.convert(remainder)


class BinaryCounter(object):
    def __init__(self):
        self.number = 0
        self.num_digits = 1
    
    def next(self):
        self.number += 1
        binary_number = int_to_binary_string(self.number)
        if len(binary_number) == self.num_digits and \
                is_all_ones(binary_number):
            self.number = 0
            self.num_digits += 1
    
    def key(self):
        """Returns the current character key in the counter."""
        
        binary_number = int_to_binary_string(self.number)
        num_leading_zeros = self.num_digits - len(binary_number)
        
        if num_leading_zeros > 0:
            binary_number = '0' * num_leading_zeros + binary_number
        
        return binary_number



class Util(object):
    """Utility functions for formatting and parsing."""

    @classmethod
    def sanitize_line(cls, line):
        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]
        return line

def open_input_file(filename):
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    return lines

def parse_args():
    args = sys.argv
    assert len(args) in (2, 3), "Provide a filename or filename plus the --test flag."

    filename = args[1]

    test_flag = False
    if len(args) == 3:
        if args[2] in ('--test', '-t'):
            test_flag = True
        else:
            assert False, "First argument should be a filename and the second either --test or -t."

    return filename, test_flag

def main():
    filename, test_flag = parse_args()
    lines = open_input_file(filename)
    
    #test_flag = True
    if test_flag:
        test_cases = [
            ["$#**\\0100000101101100011100101000", '##*\$'],
            ]
        MessageDecoding().run_tests(test_cases)
    else:
        MessageDecoding().evaluate(lines)
        
if __name__ == "__main__":
    main()
