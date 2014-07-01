import sys

class FollowingInteger(object):
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
        
    def compute(self, line, first=True):
        permutations = self.all_permutations(line)
        numbers = [int(perm) for perm in permutations]
        numbers = sorted(numbers)
        
        if not first:
            for num in numbers:
                if len(str(num)) == len(line):
                    return num
        
        seed = int(line)
        if seed == numbers[-1]:
            return self.compute(line + "0", first=False)
        else:
            index = numbers.index(seed)
            return numbers[index + 1]
        
    
    def all_permutations(self, string):
        if len(string) == 1:
            return [string]
        if len(string) == 2:
            if string[0] == string[1]:
                return [string]
            else:
                return [string, string[1] + string[0]]
        
        tr = []
        i = 0
        while i < len(string):
            char = string[i]
            remainder = string[:i] + string[i+1:]
            for perm in self.all_permutations(remainder):
                word = char + perm
                if word not in tr:
                    tr.append(word)
            i += 1
        return tr

        

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
            ['115', '151'],
            ['842', '2048'],
            ['8000', '80000'],
            ['1', '10']
            ]
        FollowingInteger().run_tests(test_cases)
    else:
        FollowingInteger().evaluate(lines)
        
if __name__ == "__main__":
    main()
