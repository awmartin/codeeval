import sys

class Top(object):
    pass
class Right(object):
    pass
class Bottom(object):
    pass
class Left(object):
    pass

sides = [Top, Right, Bottom, Left]

class SpiralOrder(object):
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)
        
    def compute(self, line):
        num_rows, num_columns, data = line.split(";")
        num_rows, num_columns, data = int(num_rows), int(num_columns), data.split(" ")
        assert len(data) == num_rows * num_columns
        matrix = self.string_to_matrix(data, num_rows, num_columns)
        elements = self.spiral(matrix)
        return " ".join(elements)
    
    def string_to_matrix(self, data, num_rows, num_columns):
        matrix = []
        for r in range(num_rows):
            row = []
            for c in range(num_columns):
                value = data[r * num_columns + c]
                row.append(value)
            matrix.append(row)
        return matrix
    
    def get_inner_matrix(self, matrix):
        if len(matrix) == 2:
            return []
        new_matrix = matrix[1:-1]
        r = 0
        for r in range(len(new_matrix)):
            new_matrix[r] = new_matrix[r][1:-1]
        assert new_matrix is not None
        return new_matrix
    
    def spiral(self, matrix):
        num_rows = len(matrix)
        num_columns = len(matrix[0])
        num_elements = num_rows * num_columns
        
        i = 0
        side = Top
        skip = num_columns
        
        tr = []
        while len(tr) < num_elements:
            r = int(i / num_columns)
            c = i % num_columns
            
            if i == 0 and side is Left:
                inner = self.get_inner_matrix(matrix)
                tr.extend(self.spiral(inner))
                return tr
                
            value = matrix[r][c]
            tr.append(value)
            
            if i == num_columns - 1 and side is Top:
                side = Right
            elif i % num_columns == 0 and side is Bottom:
                side = Left
            elif i == num_rows * num_columns - 1 and side is Right:
                side = Bottom
            
            if side is Top:
                i += 1
            elif side is Right:
                i += skip
            elif side is Bottom:
                i -= 1
            elif side is Left:
                i -= skip
        
        return tr
    
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if expected == result:
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)


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
    
    test_flag = False
    test_cases = [['3;3;1 2 3 4 5 6 7 8 9', '1 2 3 6 9 8 7 4 5'],
                  ['2;2;1 2 3 4', '1 2 4 3'],
                  ['4;4;1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16', '1 2 3 4 8 12 16 15 14 13 9 5 6 7 11 10'],
                  ['4;2;1 2 3 4 5 6 7 8', '1 2 4 6 8 7 5 3'],
                  ['4;3;1 2 3 4 5 6 7 8 9 10 11 12', '1 2 3 6 9 12 11 10 7 4 5 8'],
                  ['4;1;1 2 3 4', '1 2 3 4'],
                  ['1;4;1 2 3 4', '1 2 3 4']]
    
    if test_flag:
        SpiralOrder().run_tests(test_cases)
    else:
        SpiralOrder().evaluate(lines)
        
if __name__ == "__main__":
    main()
