import sys

class TextToNumber(object):
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if str(expected) == str(result):
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, line):
        num = Number(line)
        return num.translate()

class Number(object):
    def __init__(self, number):
        self.number = number
    
    def translate(self):
        negate = False
        if 'negative' in self.number:
            negate = True
            number = self.number.replace('negative', '')
        else:
            number = self.number
        
        millions, thousands, ones = self.split_by_magnitude(number)
        
        result = 0
        if millions is not None and millions.strip() != "":
            result += 1000000 * self.number_from_text(millions)
        if thousands is not None and thousands.strip() != "":
            result += 1000 * self.number_from_text(thousands)
        if ones is not None and ones.strip() != "":
            result += self.number_from_text(ones)
        
        if negate:
            return -result
        else:
            return result
    
    def split_by_magnitude(self, number):
        millions = None
        thousands = None
        
        if 'million' in number:
            millions, rest = number.split("million")
        else:
            rest = number
        
        if 'thousand' in rest:
            thousands, ones = rest.split("thousand")
        else:
            ones = rest
        
        return (millions, thousands, ones)
    
    value_LUT = {
              'zero': 0,
              'one': 1,
              'two': 2,
              'three': 3,
              'four': 4,
              'five': 5,
              'six': 6,
              'seven': 7,
              'eight': 8,
              'nine': 9,
              'ten': 10,
              'eleven': 11,
              'twelve': 12,
              'thirteen': 13,
              'fourteen': 14,
              'fifteen': 15,
              'sixteen': 16,
              'seventeen': 17,
              'eighteen': 18,
              'nineteen': 19,
              'twenty': 20,
              'thirty': 30,
              'forty': 40,
              'fifty': 50,
              'sixty': 60,
              'seventy': 70,
              'eighty': 80,
              'ninety': 90
              }
    
    def number_from_text(self, number):
        if number is None or number.strip() == "":
            return 0
        
        if 'hundred' in number:
            hundreds, rest = number.split("hundred")
            return self.number_from_text(hundreds) * 100 + self.number_from_text(rest)
        
        segments = [x.strip() for x in number.split(" ")]
        value = 0
        for word, word_value in self.value_LUT.iteritems():
            if word in segments:
                value += word_value
        return value
        

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
            ['fifteen', '15'],
            ['negative six hundred thirty eight', '-638'],
            ['zero', '0'],
            ['two million one hundred seven', '2000107'],
            ['nine hundred ninety nine million nine hundred ninety nine thousand nine hundred ninety nine', '999999999'],
            ['negative four hundred fourteen million nine hundred thousand four hundred seventeen', '-414900417'],
            ['negative eleven', '-11'],
            ['negative one hundred twelve', '-112'],
            ['one hundred one', '101'],
            ['fourteen', '14'],
            ['fourteen million twelve', '14000012']
            ]
        TextToNumber().run_tests(test_cases)
    else:
        TextToNumber().evaluate(lines)
        
if __name__ == "__main__":
    main()
