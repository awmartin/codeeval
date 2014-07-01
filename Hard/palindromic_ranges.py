import sys

class PalindromicRanges(object):
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
        start, end = line.split(" ")
        start = int(start)
        end = int(end)
        
        palindromes = [self.is_palindrome(x) for x in range(start, end+1)]
        return self.compute_num_ranges(palindromes)
    
    def compute_num_ranges(self, palindromes):
        count = 0
        i = 0
        while i < len(palindromes):
            j = i
            while j <= len(palindromes):
                numbers = palindromes[i:j]
                if len(numbers) == 0:
                    j += 1
                    continue
                is_interesting = sum(numbers) % 2 == 0
                if is_interesting:
                    count += 1
                j += 1
            i += 1
        return str(count)
                
    def is_palindrome(self, num_str):
        if not isinstance(num_str, str):
            num_str = str(num_str)
        
        if len(num_str) <= 1:
            return 1
        
        found_palindrome = num_str[0] == num_str[-1] and self.is_palindrome(num_str[1:-1])
        if found_palindrome:
            return 1
        
        return 0

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
            ['1 2', '1'],
            ['1 7', '12'],
            ['87 88', '1']
            ]
        PalindromicRanges().run_tests(test_cases)
    else:
        PalindromicRanges().evaluate(lines)
        
if __name__ == "__main__":
    main()
