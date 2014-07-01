import sys

class DigitStatistics(object):
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
        
    def compute(self, line):
        a, n = line.split(" ")
        a = int(a[-1])
        n = int(n)
        
        digits = self.get_digits(a, n)
        
        # Return the proper output format
        tr = []
        for d in range(10):
            if d in digits:
                tr.append(str(d) + ": " + str(digits[d]))
            else:
                tr.append(str(d) + ": 0" )
        return ", ".join(tr)
                
        
    def get_digits(self, a, n):
        if a == 0:
            return {0:n}
        if a == 1:
            return {1:n}
        if a == 2:
            # 2, 4, 8, 6 ...
            return {2:int((n+3) / 4), 4:int((n + 2) / 4), 8:int((n + 1) / 4), 6:int((n) / 4)}
        if a == 3:
            # 3, 9, 7, 1, ...
            return {3:int((n+3) / 4), 9:int((n + 2) / 4), 7: int((n + 1) / 4), 1:int((n) / 4)}
        if a == 4:
            # 4, 6, ...
            return {4:int((n+1) / 2), 6:int((n) / 2)}
        if a == 5:
            return {5: n}
        if a == 6:
            return {6: n}
        if a == 7:
            # 7, 9, 3, 1 ...
            return {7:int((n+3) / 4), 9:int((n + 2) / 4), 3:int((n + 1) / 4), 1:int((n) / 4)}
        if a == 8:
            # 8, 4, 2, 6 ...
            return {8:int((n+3) / 4), 4:int((n + 2) / 4), 2:int((n + 1) / 4), 6:int((n) / 4)}
        if a == 9:
            # 9, 1 ...
            return {9:int((n+1) / 2), 1:int((n) / 2)}
        assert False
    
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
            ['2 5', '0: 0, 1: 0, 2: 2, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0']
            ]
        DigitStatistics().run_tests(test_cases)
    else:
        DigitStatistics().evaluate(lines)
        
if __name__ == "__main__":
    main()
