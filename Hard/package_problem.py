import sys


class PackageProblem(object):
    def __init__(self):
        self.cache = {}
    
    def evaluate(self, lines):
        for line in lines:
            line = Util.sanitize_line(line)
            self.cache = {}
            print self.compute(line)
        
    def run_tests(self, test_cases):
        for input, expected in test_cases:
            result = self.compute(input)
            if expected == result:
                print "Test passed: %s" % input
            else:
                print "Test failed: Expected %s and got %s" % (expected, result)
        
    def compute(self, line):
        capacity, items = line.split(":")
        capacity = int(capacity.strip())
        
        items = items.strip().split(" ")
        items = [Item.parse(item) for item in items]
        
        # Maximize cost but within the total weight capacity.
        
        total_cost, in_the_box = self.knapsack(len(items)-1, items, capacity, [])
        if len(in_the_box) == 0:
            return '-'
        ids = [str(item.index) for item in in_the_box]
        return ",".join(sorted(ids))
        
        
    def knapsack(self, n, items, capacity, in_the_box=[]):
        key = (n, capacity)
        if key in self.cache:
            return self.cache[key]
        
        if n == 0 or capacity <= 0:
            return 0, in_the_box
        
        # Exclude nth item.
        case1, excluding = self.knapsack(n-1, items[:n] + items[n+1:], capacity, in_the_box)
        
        # Include the nth item.
        item = items[n]
        cost2, in_the_box_2 = self.knapsack(n-1, items[:n] + items[n+1:], capacity-item.weight, in_the_box)
        case2 = item.cost + cost2
        including = in_the_box_2 + [item]
        
        which_case = max(case1, case2)
        if which_case == case2 and item.weight < capacity:
            key = (n, capacity)
            self.cache[key] = (case2, including)
            return case2, including
        else:
            key = (n, capacity)
            self.cache[key] = (case1, excluding)
            return case1, excluding


class Item(object):
    def __init__(self, index, weight, cost):
        self.index = int(index)
        self.weight = float(weight)
        self.cost = int(cost.replace("$", ""))
    
    @classmethod
    def parse(cls, group):
        group = group[1:-1]
        values = group.split(",")
        return cls(*values)



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
    
    # test_flag = True
    if test_flag:
        test_cases = [
            ["81 : (1,53.38,$45) (2,88.62,$98) (3,78.48,$3) (4,72.30,$76) (5,30.18,$9) (6,46.34,$48)", '4'],
            ['8 : (1,15.3,$34)', '-'],
            ['75 : (1,85.31,$29) (2,14.55,$74) (3,3.98,$16) (4,26.24,$55) (5,63.69,$52) (6,76.25,$75) (7,60.02,$74) (8,93.18,$35) (9,89.95,$78)', '2,7'],
            ['56 : (1,90.72,$13) (2,33.80,$40) (3,43.15,$10) (4,37.97,$16) (5,46.81,$36) (6,48.77,$79) (7,81.80,$45) (8,19.36,$79) (9,6.76,$64)', '8,9']
            ]
        PackageProblem().run_tests(test_cases)
    else:
        PackageProblem().evaluate(lines)
        
if __name__ == "__main__":
    main()
