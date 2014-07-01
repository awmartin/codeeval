import sys

class ClimbingStairs(object):
    def __init__(self):
        self.computed = {}
    
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
        num_steps = int(line)
        if num_steps == 1:
            return 1
        if num_steps == 2:
            return 2
        
        # Cache values for performance.
        if num_steps in self.computed:
            return self.computed[num_steps]
        else:
            one_step = self.compute(num_steps - 1)
            two_steps = self.compute(num_steps - 2)
            new_steps = one_step + two_steps
            self.computed[num_steps] = new_steps
            return new_steps

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
            ['10', '89'],
            ['20', '10946'],
            ]
        ClimbingStairs().run_tests(test_cases)
    else:
        ClimbingStairs().evaluate(lines)
        
if __name__ == "__main__":
    main()
