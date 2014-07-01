import sys

class MineSweeper(object):
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
        dims, field_str = line.split(";")
        num_rows, num_columns = dims.split(",")
        
        field = Field(field_str, num_rows, num_columns)
        return field.mine_field_str()
        
        
class Field(object):
    def __init__(self, field_str, num_rows, num_columns):
        self.field_str = field_str
        self.num_rows = int(num_rows)
        self.num_columns = int(num_columns)
        
        self.field = None
        
        self.dummy_cell = Cell(-1, -1, False, self)
        
        self.build_field()
    
    def build_field(self):
        self.field = []
        for r in range(self.num_rows):
            row = []
            for c in range(self.num_columns):
                cell_type = self.field_str[r * self.num_columns + c]
                row.append(Cell(r, c, cell_type == '*', self))
            self.field.append(row)
    
    def mine_field_str(self):
        tr = ""
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                tr += str(self.field[r][c].count())
        return tr
    
    
    def get_cell(self, r, c):
        if r < 0 or r >= self.num_rows or c < 0 or c >= self.num_columns:
            return self.dummy_cell
        return self.field[r][c]
        
        
class Cell(object):
    def __init__(self, row, column, is_mine, field):
        self.row = row
        self.column = column
        self.is_mine = is_mine
        self.field = field
            
    def count(self):
        if self.is_mine:
            return "*"
            
        neighborhood = []
        indices = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for pair in indices:
            cell = self.field.get_cell(pair[0] + self.row, pair[1] + self.column)
            neighborhood.append(cell)
        
        count = 0
        for cell in neighborhood:
            if cell.is_mine:
                count += 1
        return count


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
            ['3,5;**.........*...', '**100332001*100'],
            ['4,4;*........*......', '*10022101*101110']
            ]
        MineSweeper().run_tests(test_cases)
    else:
        MineSweeper().evaluate(lines)
        
if __name__ == "__main__":
    main()
