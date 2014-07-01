
import re
import sys


class Node(object):
    def __init__(self, string, left=None, right=None, operation=None, parent=None):
        self.string = string
        self.value = None
        self.left = None
        self.right = None
        self.operation = None
        self.parent = None

    def is_splittable(self):
        return len(self.string) > 1 and (self.left is None and self.right is None)

    def has_splittable_descendant(self):
        pass

    def evaluate(self):
        if self.value is not None:
            return

        if self.operation is None:
            self.value = int(self.string)
        else:
            self.left.evaluate()
            self.right.evaluate()

            if self.operation == '+':
                self.value = self.left.value + self.right.value
            if self.operation == '-':
                self.value = self.left.value - self.right.value

    def split(self):
        if self.is_splittable():
            left_str = self.string[:-1]
            self.left = Node(left_str)
            self.left.parent = self

            right_str = self.string[-1]
            self.right = Node(right_str)
            self.right.parent = self

            self.operation = '+'
            self.value = None

    def minus(self):
        self.operation = '-'

    def shift(self):
        if self.left is not None and self.right is not None:
            self.reset()

            self.left.reconstitute()
            self.right.reconstitute()

            if len(self.left.string) > 1:
                to_shift = self.left.string[-1]
                self.left.string = self.left.string[:-1]
                self.right.string = to_shift + self.right.string

    def reconstitute(self):
        """Recombines the entire tree into a single node."""

        if self.left is not None and self.right is not None:
            self.left.reconstitute()
            self.right.reconstitute()

            self.string = self.left.string + self.right.string

            self.value = None
            self.operation = None
            self.left = None
            self.right = None

    def reset(self):
        self.value = None


class Visitor(object):
    def __init__(self, node):
        self.root = node


    def traverse(self, node):
        if node.is_spliitable():
            pass

    def split(self, node):
        pass


class UglyNumbers(object):
    def __init__(self):
        self.operator_regex = re.compile('[+-]')
        self.leading_zeros = re.compile('^[0]*([1-9]*)')

    def evaluate(self, lines):
        for line in lines:
            if len(line.strip()) == 0:
                continue

            print self.compute(line)

    def compute(self, line):
        line = Util.sanitize_line(line)
        node = Node(line)

        node.evaluate()

        node.split()
        node.evaluate()

        return 0

    def remove_octals(self, expr):
        values = self.operator_regex.split(expr)
        operators = self.operator_regex.findall(expr)
        values = [self.strip_leading_zeros(val) for val in values]

        i = 0
        tr = ""
        while i < len(values):
            val = values[i]
            tr += val
            if i < len(operators):
                op = operators[i]
                tr += op
            i += 1
        return tr

    def strip_leading_zeros(self, value):
        new_val = self.leading_zeros.match(value).groups()[0]
        if new_val == "":
            return '0'
        return new_val

    # 1+1+1
    # 1+1-1
    # 1+11
    # 1-1+1
    # 1-1-1
    # 1-11
    # 11+1
    # 11-1
    # 111

    def produce_expressions(self, line):
        if len(line) == 0:
            return []
        if len(line) == 1:
            return [line]

        operations = ['+', '-', '']

        expressions = []
        digit = line[0]
        remainder = line[1:]

        for op in operations:
            tr = digit
            tr += op
            for expr in self.produce_expressions(remainder):
                to_add = tr + expr
                expressions.append(to_add)

        return expressions

    def run_tests(self, test_cases):
        pass

    def is_ugly(self, number):
        return number % 2 == 0 or \
                number % 3 == 0 or \
                number % 5 == 0 or \
                number % 7 == 0


class Operation(object):
    pass
class Add(Operation):
    def compute(self, x, y):
        return x + y
class Subtract(Operation):
    def compute(self, x, y):
        return x - y
class Noop(Operation):
    def compute(self, x, y):
        return 10 * x + y


class Util(object):
    @classmethod
    def sanitize_line(cls, line):
        line = line.replace(" ", "")

        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]

        return line

# ---------------------------------------------------------------------------------------------
# Functions for actually running the program.

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

    if test_flag:
        UglyNumbers().run_tests(lines)
    else:
        UglyNumbers().evaluate(lines)

if __name__ == "__main__":
    main()



