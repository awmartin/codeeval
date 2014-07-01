import sys


class LargestSubmatrix(object):
    def __init__(self):
        self.cache = {}
    
    def evaluate(self, lines):
        lines = [Util.sanitize_line(line) for line in lines]
        rows = [line.split(" ") for line in lines]
        rows = [[int(x) for x in row] for row in rows]
        matrix = Matrix(rows)
        print self.compute(matrix)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if expected == result:
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, matrix):
        m = 0
        size = len(matrix.rows)
        
        for r1 in range(0, size):
            for r2 in range(r1, size):
                for c1 in range(0, size):
                    for c2 in range(c1, size):
                        m = max(m, matrix.sum(r1, r2, c1, c2))
        return m


class Matrix(object):
    def __init__(self, rows):
        self.rows = rows
        self.size = len(rows)
    
    def __getitem__(self, cell):
        if isinstance(cell, tuple):
            return self.rows[cell[0]][cell[1]]
            
        elif isinstance(cell, int):
            return self.rows[cell]

    def sum(self, r1, r2, c1, c2):
        s = 0
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                s += self.rows[r][c]
        return s


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
            ["", ''],
            ]
        LargestSubmatrix().run_tests(test_cases)
    else:
        LargestSubmatrix().evaluate(lines)
        
if __name__ == "__main__":
    main()
