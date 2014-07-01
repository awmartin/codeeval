import sys

class Skyscrapers(object):
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
        building_strs = [bldg.strip() for bldg in line.split(";")]
        buildings = [self.parse_building(bldg_str) for bldg_str in building_strs]
        
        left_min = min([bldg.left for bldg in buildings])
        right_max = max([bldg.right for bldg in buildings])
        
        # Height array
        arr = [0 for i in range(left_min, right_max + 1)]
        
        for building in buildings:
            # If building.left == 1, that means the interval btw 1 and 2
            for i in range(building.left, building.right):
                arr[i-left_min] = max(arr[i-left_min], building.height)
        
        # Convert to the proper format.
        pt_array = self.height_array_to_point_array(arr, left_min)
        
        pt_array = [str(i) for i in pt_array]
        return " ".join(pt_array)
        
    def height_array_to_point_array(self, arr, left_min):

        current_height = arr[0]
        pts = [left_min, current_height]
                
        for i in range(1, len(arr)):
            height = arr[i]
            if current_height != height:
                pts.append(i + left_min)
                pts.append(height)
                current_height = height
        
        return pts
    
    def parse_building(self, bldg_str):
        bldg_str = bldg_str.strip()[1:-1]
        left, height, right = bldg_str.split(",")
        return Building(left, height, right)

class Building(object):
    def __init__(self, left, height, right):
        self.left = int(left)
        self.height = int(height)
        self.right = int(right)
    

    
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
            ['(1,2,3);(2,4,6);(4,5,5);(7,3,11);(9,2,14);(13,7,15);(14,3,17)',
                 '1 2 2 4 4 5 5 4 6 0 7 3 11 2 13 7 15 3 17 0'],
            ['(2,22,3);(6,12,10);(15,6,21)',
                 '2 22 3 0 6 12 10 0 15 6 21 0'],
            ['(1,2,6);(9,23,22);(22,6,24);(8,14,19);(23,12,30)',
                 '1 2 6 0 8 14 9 23 22 6 23 12 30 0']
            ]
        Skyscrapers().run_tests(test_cases)
    else:
        Skyscrapers().evaluate(lines)
        
if __name__ == "__main__":
    main()
