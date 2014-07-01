import sys


class MinimumPathSum(object):
    def __init__(self):
        self.cache = {}
    
    def evaluate(self, lines):
        lines = [Util.sanitize_line(line) for line in lines]
        matrices = Parser().parse(lines)
        
        for matrix in matrices:
            self.cache = {}
            print self.compute(matrix)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if expected == result:
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, matrix):
        paths = self.paths_from_matrix(matrix, Cell(0, 0))
        return min(paths)
    
    def paths_from_matrix(self, matrix, pos):
        key = (pos.x, pos.y)
        if key in self.cache:
            return self.cache[key]
        
        value = matrix[pos]
        
        directions = [Cell(1, 0), Cell(0, 1)]
        
        dim = matrix.size - 1
        if pos == Cell(dim, dim):
            return [value]
        if pos.x == dim:
            directions = [Cell(0, 1)]
        if pos.y == dim:
            directions = [Cell(1, 0)]
        
        # ---------------------------------------------------------
        
        paths = []
        for direction in directions:
            next_pos = pos + direction
            
            # Get all the subpaths starting from 'next_pos'.
            subpaths = self.paths_from_matrix(matrix, next_pos)
            key = (next_pos.x, next_pos.y)
            self.cache[key] = subpaths
            
            # Add the current pos to all the paths.
            subpaths = [value+sp for sp in subpaths]
            paths.extend(subpaths)
            
            
        
        return paths


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
     
    def __str__(self):
        return "Cell(%s, %s)" % (self.x, self.y)
    
    def __getitem__(self, coord):
        if coord == 0:
            return self.x
        elif coord == 1:
            return self.y
        return None
    
    def __add__(self, other):
        return Cell(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Matrix(object):
    def __init__(self, rows):
        self.rows = rows
        self.size = len(rows)
    
    def __getitem__(self, cell):
        if isinstance(cell, Cell):
            return self.rows[cell[0]][cell[1]]
            
        elif isinstance(cell, tuple):
            return self.rows[cell[0]][cell[1]]
            
        elif isinstance(cell, int):
            return self.rows[cell]


class Parser(object):
    def __init__(self):
        pass
    
    def parse(self, lines):
        matrices = []
        
        i = 0
        while i < len(lines):
            matrix_size = int(lines[i])
            
            matrix_rows = lines[i + 1:i + 1 + matrix_size]
            matrix_rows = [row.split(",") for row in matrix_rows]
            matrix_rows = [[int(x) for x in row] for row in matrix_rows]
            matrices.append(Matrix(matrix_rows))
            
            i += (1 + len(matrix_rows))
        
        return matrices


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
        MinimumPathSum().run_tests(test_cases)
    else:
        MinimumPathSum().evaluate(lines)
        
if __name__ == "__main__":
    main()
